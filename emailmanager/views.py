import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from auth_api.auth_token import CustomRequest, login_token_required
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
