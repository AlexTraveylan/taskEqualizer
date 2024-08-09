from django.http import JsonResponse
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from emailmanager.crypto import encrypt
from tasks_api.member.schemas import MemberSchemaIn

router = Router()


@router.get("/", tags=["member"])
@login_token_required
def who_i_am(request: CustomRequest):
    """Display actual member"""

    return JsonResponse({"member_id": str(request.member.id)}, status=200)


@router.put("/", tags=["member"])
@login_token_required
def update_member(request: CustomRequest, payload: MemberSchemaIn):
    """Update a member."""

    if payload.email is not None:
        request.member.email = encrypt(payload.email)

    request.member.member_name = payload.member_name
    request.member.save()

    return JsonResponse({"message": "Member updated successfully."}, status=200)


@router.delete("/{member_id}", tags=["member"])
@login_token_required
def delete_member(request: CustomRequest, member_id: str):
    """Delete a member."""

    members_in_family = request.member.family.members.all()

    if member_id not in [str(member.id) for member in members_in_family]:
        return JsonResponse({"message": "Member not found."}, status=404)

    member = members_in_family.get(id=member_id)
    member.delete()
    response = JsonResponse({"message": "Member deleted successfully."}, status=200)

    return response
