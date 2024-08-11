from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from emailmanager.crypto import generate_confirmation_token
from emailmanager.models import EmailConfirmationToken
from emailmanager.send_email import (
    html_wrapper_for_confirmation_email_with_token,
    send_contact_message,
)
from tasks_api.member.schemas import MemberSchemaIn

router = Router()


@router.get("/", tags=["member"])
@login_token_required
def who_i_am(request: CustomRequest):
    """Display actual member"""

    return JsonResponse({"member_id": str(request.member.id)}, status=200)


@router.put("/", tags=["member"])
@transaction.atomic
@login_token_required
def update_member(request: CustomRequest, payload: MemberSchemaIn):
    """Update a member."""

    if payload.email is not None and payload.email != request.member.email:
        token = generate_confirmation_token()
        confirmation = EmailConfirmationToken.objects.create(
            member=request.member,
            encrypted_email=payload.email,
            token=token,
        )
        html = html_wrapper_for_confirmation_email_with_token(token)
        send_contact_message(
            subject="TaskEqualizer - Confirm your email address",
            html=html,
            to=confirmation.get_email(),
        )

    user = User.objects.filter(username=payload.member_name)

    if request.member.member_name != payload.member_name and len(user) > 0:
        return JsonResponse({"message": "Username already exists."}, status=400)

    user = User.objects.get(username=request.member.member_name)
    user.username = payload.member_name
    user.save()
    request.member.member_name = payload.member_name
    request.member.save()

    return JsonResponse({"message": "Member updated successfully."}, status=200)


@router.delete("/{member_id}", tags=["member"])
@transaction.atomic
@login_token_required
def delete_member(request: CustomRequest, member_id: str):
    """Delete a member."""

    members_in_family = request.member.family.members.all()

    if member_id not in [str(member.id) for member in members_in_family]:
        return JsonResponse({"message": "Member not found."}, status=404)

    member = members_in_family.get(id=member_id)
    user = User.objects.get(username=member.member_name)
    user.delete()
    member.delete()

    response = JsonResponse({"message": "Member deleted successfully."}, status=200)

    return response
