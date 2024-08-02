"""This module contains the views for the tasks_api app."""

import json
from typing import Literal

import stripe
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import Schema

from auth_api.auth_token import CustomRequest, login_token_required
from subscriptions.models import Subscription
from subscriptions.sub_types import (
    CHANGE_PLAN_SURCHARGE,
    SUBSCRIPTION_PLANS_RESTRICTIONS,
    PaymentStatusChoices,
)
from TaskEqualizer.settings import STRIP_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from tasks_api.family_settings.models import FamilySettings

stripe.api_key = STRIP_SECRET_KEY


class AmountSchemaIn(Schema):
    amount_cent: int
    souscription_plan: Literal["BASIC", "PREMIUM"]


@csrf_exempt
@login_token_required
def create_checkout_session(request: CustomRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    family_settings = FamilySettings.objects.filter(
        family=request.member.family
    ).first()

    if family_settings.subscription_plan == "PREMIUM":
        return JsonResponse(
            {"error": "Already subscribed to the PREMIUM plan"}, status=400
        )

    data = json.loads(request.body)
    plan = data["souscription_plan"]

    if family_settings.subscription_plan == "BASIC" and plan == "BASIC":
        return JsonResponse(
            {"error": "Already subscribed to the BASIC plan"}, status=400
        )

    amount_cent = SUBSCRIPTION_PLANS_RESTRICTIONS[plan]["amount_cent"] * (
        1 - SUBSCRIPTION_PLANS_RESTRICTIONS[plan]["reduction"]
    )

    if family_settings.subscription_plan == "BASIC" and plan == "PREMIUM":
        amount_cent -= (
            SUBSCRIPTION_PLANS_RESTRICTIONS["BASIC"]["amount_cent"]
            * (1 - SUBSCRIPTION_PLANS_RESTRICTIONS["BASIC"]["reduction"])
        ) - CHANGE_PLAN_SURCHARGE

        print(amount_cent)

    payload = AmountSchemaIn(
        amount_cent=amount_cent,
        souscription_plan=plan,
    )

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(payload.amount_cent),
            currency="eur",
            payment_method_types=["card"],
        )

        Subscription.objects.create(
            amount=payload.amount_cent,
            stripe_transaction_id=intent.id,
            status=PaymentStatusChoices.PENDING,
            subscription_plan=payload.souscription_plan,
            member_id=str(request.member.id),
            family=request.member.family,
        )

        return JsonResponse({"client_secret": intent.client_secret})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def stripe_webhook(request: HttpRequest):
    payload = request.body
    sig_header = request.headers["STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        # Invalid payload
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]

        subcription = Subscription.objects.get(
            stripe_transaction_id=payment_intent["id"]
        )
        subcription.status = PaymentStatusChoices.PAID
        subcription.family
        subcription.save()

        family_setting = FamilySettings.objects.filter(
            family=subcription.family
        ).first()
        family_setting.subscription_plan = subcription.subscription_plan
        family_setting.save()

    elif event["type"] in ("payment_intent.payment_failed", "payment_intent.canceled"):
        payment_intent = event["data"]["object"]

        subcription = Subscription.objects.get(
            stripe_transaction_id=payment_intent["id"]
        )
        subcription.status = PaymentStatusChoices.FAILED
        subcription.save()

    else:
        print("Unhandled event type {}".format(event["type"]))

    return JsonResponse({"status": "success"})


@csrf_exempt
def get_plans_informations(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    return JsonResponse(SUBSCRIPTION_PLANS_RESTRICTIONS, status=200)
