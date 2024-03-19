from django.http import JsonResponse
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.family.schemas import FamilySchemaIn

router = Router()


@router.get("/members/", tags=["family"])
@login_token_required
def list_members_by_family(request: CustomRequest):
    """List all members by family."""

    family = request.member.family

    members = family.members.all()
    members_dict = list(members.values())

    reponse = JsonResponse(members_dict, safe=False, status=200)
    reponse.set_cookie("auth_token", request.auth_token)

    return reponse


@router.get(
    "/possibles_tasks/",
    tags=["family"],
)
@login_token_required
def list_possibles_tasks_by_family(request: CustomRequest):
    """List all possible tasks by family."""

    possible_tasks = request.member.family.possible_tasks.all()
    possible_tasks_dict = list(possible_tasks.values())

    reponse = JsonResponse(possible_tasks_dict, safe=False, status=200)
    reponse.set_cookie("auth_token", request.auth_token)

    return reponse


@router.get("/", tags=["family"])
@login_token_required
def retrieve_family(request: CustomRequest):
    """Retrieve a family."""

    response = JsonResponse(request.member.family.to_dict(), status=200)
    response.set_cookie("auth_token", request.auth_token)

    return response


@router.put("/", tags=["family"])
@login_token_required
def update_family(request: CustomRequest, payload: FamilySchemaIn):
    """Update a family."""

    family = request.member.family

    for key, value in payload.dict().items():
        setattr(family, key, value)

    family.save()

    reponse = JsonResponse({"message": "Family updated successfully."}, status=200)
    reponse.set_cookie("auth_token", request.auth_token)

    return reponse


@router.delete("/", tags=["family"])
@login_token_required
def delete_family(request: CustomRequest):
    """Delete a family."""

    request.member.family.delete()
    request.delete_cookie("auth_token")

    return {"message": "Family deleted successfully."}
