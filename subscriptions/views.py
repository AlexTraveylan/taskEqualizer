"""This module contains the views for the tasks_api app."""

import json

import stripe
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import Schema

from TaskEqualizer.settings import CLIENT_HOST, STRIP_SECRET_KEY, STRIPE_WEBHOOK_SECRET

stripe.api_key = STRIP_SECRET_KEY


class AmountSchemaIn(Schema):
    amount: float


@csrf_exempt
def create_checkout_session(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    payload = AmountSchemaIn(amount=data["amount"])

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": "Abonnement",
                        },
                        "unit_amount_decimal": payload.amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=CLIENT_HOST
            + "/http://localhost:3000/en/commun/settings/payment-success/",
            cancel_url=CLIENT_HOST + "/commun/settings/payment-failed/",
        )
        return JsonResponse({"id": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@csrf_exempt
def stripe_webhook(request: HttpRequest):
    payload = request.body
    sig_header = request.headers["STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
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
    # ... handle other event types
    else:
        print("Unhandled event type {}".format(event["type"]))

    return JsonResponse({"status": "success"})
