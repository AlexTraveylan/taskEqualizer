import random
from datetime import datetime, timedelta

from django.http import JsonResponse
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
    expire_date_one_week = datetime.now() + timedelta(days=7)

    new_invitation = Invitation.objects.create(
        code=new_code, family=request.member.family, expired_at=expire_date_one_week
    )

    response = JsonResponse(new_invitation.to_dict(), status=201)
    response.set_cookie(
        "auth_token", request.auth_token, httponly=True, secure=True, samesite=None
    )

    return response
