import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.invitation.models import Invitation

router = Router()


def create_random_invitation_code() -> str:
    """A fonction creating a random code for an invitation
    8 characters long, composed of uppercase letters and numbers.

    Exemples
    --------
    >>> create_random_invitation_code()
    'JFK12DSQ'

    Returns:
        str: A random code for an invitation
    """
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))


@router.get("/", tags=["invitation"])
@login_token_required
def create_invitation(request: CustomRequest):
    """Create an invitation."""

    new_code = create_random_invitation_code()
    expire_date_one_week = timezone.now() + timezone.timedelta(days=7)
    print(expire_date_one_week)

    new_invitation = Invitation.objects.create(
        code=new_code, family=request.member.family, expired_at=expire_date_one_week
    )

    return JsonResponse(new_invitation.to_dict(), status=201)


@router.get("/get_valid_list/", tags=["invitation"])
@login_token_required
def get_valid_invitation_list(request: CustomRequest):
    """Get a list of valid invitations."""

    not_expired_invitations = Invitation.objects.filter(
        family=request.member.family, expired_at__gt=timezone.now()
    )

    invitations = [invitation.to_dict() for invitation in not_expired_invitations]

    return JsonResponse({"data": invitations}, status=200)


@router.delete("/{invitation_id}", tags=["invitation"])
@login_token_required
def delete_invitation(request: CustomRequest, invitation_id: str):
    """Delete an invitation."""

    invitation = get_object_or_404(
        Invitation, id=invitation_id, family=request.member.family
    )

    invitation.delete()

    return JsonResponse({"message": "Invitation deleted"}, status=200)


@router.delete("/clean_invitations/", tags=["invitation"])
@login_token_required
def clean_invitations(request: CustomRequest):
    """Delete all expired and unused invitations."""

    expired_invitations = Invitation.objects.filter(
        expired_at__lt=timezone.now(), is_used=False, family=request.member.family
    )

    expired_invitations.delete()

    return JsonResponse(
        {"message": "Expired and unused invitations deleted"}, status=200
    )
