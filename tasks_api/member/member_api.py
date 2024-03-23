from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.member.models import Member
from tasks_api.member.schemas import MemberSchemaIn, MemberSchemaOut
from tasks_api.task.schemas import TaskSchemaOut

router = Router()


@router.get("/tasks/{member_id}", response=list[TaskSchemaOut], tags=["member"])
def list_member_tasks(request: HttpRequest, member_id: str):
    """List all tasks for a member."""
    member = get_object_or_404(Member, id=member_id)

    tasks = member.tasks.all()

    return tasks


@router.get("/{member_id}", response=MemberSchemaOut, tags=["member"])
def retrieve_member(request: HttpRequest, member_id: str):
    """Retrieve a member."""

    member = get_object_or_404(Member, id=member_id)

    return member


@router.put("/{member_id}", tags=["member"])
@login_token_required
def update_member(request: CustomRequest, member_id: str, payload: MemberSchemaIn):
    """Update a member."""

    for key, value in payload.dict().items():
        setattr(request.member, key, value)

    request.member.save()
    response = JsonResponse({"message": "Member updated successfully."}, status=200)
    response.set_cookie("auth_token", request.auth_token, httponly=True)

    return request.member


@router.delete("/{member_id}", tags=["member"])
@login_token_required
def delete_member(request: CustomRequest, member_id: str):
    """Delete a member."""

    request.member.delete()

    reponse = JsonResponse({"message": "Member deleted successfully."}, status=200)
    reponse.delete_cookie("auth_token")

    return reponse
