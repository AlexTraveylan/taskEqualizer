from django.shortcuts import get_object_or_404
from ninja import Router

from tasks_api.models import Member
from tasks_api.schemas import MemberSchemaIn, MemberSchemaOut, TaskSchemaOut

router = Router()


@router.post("/", response=MemberSchemaOut, tags=["member"])
def create_member(request, payload: MemberSchemaIn):
    """Create a member."""

    new_member = Member.objects.create(**payload.dict())

    return new_member


@router.get("/", response=list[MemberSchemaOut], tags=["member"])
def list_members(request):
    """List all members."""
    members = Member.objects.all()

    return members


@router.get("/tasks/{member_id}", response=list[TaskSchemaOut], tags=["member"])
def list_member_tasks(request, member_id: int):
    """List all tasks for a member."""
    member = get_object_or_404(Member, id=member_id)

    tasks = member.tasks.all()

    return tasks


@router.get("/{member_id}", response=MemberSchemaOut, tags=["member"])
def retrieve_member(request, member_id: str):
    """Retrieve a member."""

    member = get_object_or_404(Member, id=member_id)

    return member


@router.put("/{member_id}", response=MemberSchemaOut, tags=["member"])
def update_member(request, member_id: int, payload: MemberSchemaIn):
    """Update a member."""

    member = get_object_or_404(Member, id=member_id)

    for key, value in payload.dict().items():
        setattr(member, key, value)

    member.save()

    return member


@router.delete("/{member_id}", tags=["member"])
def delete_member(request, member_id: int):
    """Delete a member."""

    member = get_object_or_404(Member, id=member_id)

    member.delete()

    return {"message": "Member deleted successfully."}
