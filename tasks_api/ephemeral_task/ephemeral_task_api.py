from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.ephemeral_task.models import EphemeralTask
from tasks_api.ephemeral_task.schemas import (
    EphemeralTaskSchemaIn,
    EphemeralTaskSchemaOut,
)

router = Router()


@router.get("/", tags=["ephemeral_task"])
@login_token_required
def get_all_ephemeral_tasks_for_family(request: CustomRequest):
    e_tasks = EphemeralTask.objects.filter(family=request.member.family)

    data = {"data": [task.to_dict() for task in e_tasks]}

    return JsonResponse(data=data, status=200)


@router.post("/", tags=["ephemeral_task"], response={201: EphemeralTaskSchemaOut})
@login_token_required
def create_ephemeral_task(request: CustomRequest, payload: EphemeralTaskSchemaIn):
    """Create a new ephemeral task."""

    task = EphemeralTask.objects.create(
        ephemeral_task_name=payload.ephemeral_task_name,
        description=payload.description,
        value=payload.value,
        family=request.member.family,
    )

    return JsonResponse(task.to_dict(), status=201)


@router.put("/{ephemeral_task_id}", tags=["ephemeral_task"])
@login_token_required
def update_ephemeral_task(request: CustomRequest, ephemeral_task_id: str):
    e_task = get_object_or_404(EphemeralTask, id=ephemeral_task_id)

    if request.member.family != e_task.family or e_task.ended_at is not None:
        return JsonResponse(
            {"message": "You are not allowed to access this ephemeral task."},
            status=403,
        )

    e_task.ended_at = timezone.now()
    e_task.member = request.member
    e_task.save()

    return JsonResponse(e_task.to_dict(), status=200)


@router.delete("/{ephemeral_task_id}", tags=["ephemeral_task"])
@login_token_required
def delete_ephemeral_task(request: CustomRequest, ephemeral_task_id: str):
    e_task = get_object_or_404(EphemeralTask, id=ephemeral_task_id)

    if e_task.member is not None:
        return JsonResponse(
            {"message": "Task already done, you can't delete it."},
            status=403,
        )

    if e_task.family != request.member.family:
        return JsonResponse(
            {"message": "You are not allowed to access this ephemeral task."},
            status=403,
        )

    e_task.delete()

    return JsonResponse({"message": "Ephemeral Task deleted"}, status=200)
