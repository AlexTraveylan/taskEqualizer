from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.family.models import Family
from tasks_api.family.schemas import FamilySchemaIn

router = Router()


@login_token_required
@router.get("/{family_id}/members/", tags=["family"])
def list_members_by_family(request: CustomRequest, family_id: int):
    """List all members by family."""

    family = get_object_or_404(Family, id=family_id)

    if request.member.family != family:
        return JsonResponse(
            {"message": "You are not allowed to access this family."}, status=403
        )

    members = family.members.all()
    members_dict = [member.to_dict() for member in members]

    reponse = JsonResponse(members_dict, status=200)
    reponse.set_cookie("auth_token", request.auth_token)

    return reponse


@login_token_required
@router.get(
    "/{family_id}/possibles_tasks/",
    tags=["family"],
)
def list_possibles_tasks_by_family(request: CustomRequest, family_id: int):
    """List all possible tasks by family."""

    family = get_object_or_404(Family, id=family_id)

    if request.member.family != family:
        return JsonResponse(
            {"message": "You are not allowed to access this family."}, status=403
        )

    possible_tasks = family.possible_tasks.all()
    possible_tasks_dict = [possible_task.to_dict() for possible_task in possible_tasks]

    reponse = JsonResponse(possible_tasks_dict, status=200)
    reponse.set_cookie("auth_token", request.auth_token)

    return reponse


@login_token_required
@router.get("/{family_id}", tags=["family"])
def retrieve_family(request: CustomRequest, family_id: int):
    """Retrieve a family."""

    family = get_object_or_404(Family, id=family_id)

    if request.member.family != family:
        return JsonResponse(
            {"message": "You are not allowed to access this family."}, status=403
        )

    response = JsonResponse(family.to_dict(), status=200)
    response.set_cookie("auth_token", request.auth_token)

    return response


@login_token_required
@router.put("/{family_id}", tags=["family"])
def update_family(request: CustomRequest, family_id: int, payload: FamilySchemaIn):
    """Update a family."""

    family = get_object_or_404(Family, id=family_id)

    if request.member.family != family:
        return JsonResponse(
            {"message": "You are not allowed to access this family."}, status=403
        )

    for key, value in payload.dict().items():
        setattr(family, key, value)

    family.save()

    reponse = JsonResponse({"message": "Family updated successfully."}, status=200)
    reponse.set_cookie("auth_token", request.auth_token)

    return reponse


@login_token_required
@router.delete("/{family_id}", tags=["family"])
def delete_family(request: CustomRequest, family_id: int):
    """Delete a family."""

    family = get_object_or_404(Family, id=family_id)

    if request.member.family != family:
        return JsonResponse(
            {"message": "You are not allowed to access this family."}, status=403
        )

    family.delete()

    return {"message": "Family deleted successfully."}
