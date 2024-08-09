import json

from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from auth_api.auth_token import CustomRequest, login_token_required
from emailmanager.models import EmailConfirmationToken
from emailmanager.schemas import ContactFormSchema
from emailmanager.send_email import html_wrapper_for_mail, send_contact_message


@csrf_exempt
@login_token_required
def contact_email_view(request: CustomRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)

    try:
        contact_form = ContactFormSchema(**data)
    except (ValueError, ValidationError):
        return JsonResponse({"error": "Invalid data"}, status=400)

    html = html_wrapper_for_mail(contact_form.message)
    subject = f"Contact from {request.member.member_name} ({request.member.id} : {contact_form.email})"
    try:
        response = send_contact_message(subject, html)
        response["id"]
    except Exception:
        return JsonResponse({"error": "Failed to send email"}, status=500)

    return JsonResponse({"message": "Email sent"}, status=200)


@csrf_exempt
def confirm_email_view(request: HttpRequest, token: str):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    confirmation = get_object_or_404(EmailConfirmationToken, token=token)
    confirmation.is_confirmed = True
    confirmation.save()

    confirmation.member.email = confirmation.get_email()
    confirmation.member.save()

    user = User.objects.get(username=confirmation.member.member_name)
    user.email = confirmation.get_email()
    user.save()

    return JsonResponse({"message": "Email confirmed"}, status=200)
