from datetime import datetime, timezone

from django.http import HttpRequest, JsonResponse
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.task.models import Task
from tasks_api.task.schemas import TaskSchemaIn, TaskSchemaOut

router = Router()


@router.post("/", tags=["task"])
@login_token_required
def create_task(request: CustomRequest, payload: TaskSchemaIn):
    """Create a task."""

    new_task = Task.objects.create(
        related_possible_task_id=payload.related_possible_task_id, member=request.member
    )

    response = JsonResponse(new_task.to_dict(), status=201)
    response.set_cookie("auth_token", request.auth_token, httponly=True)

    return response


@router.get("/", tags=["task"])
@login_token_required
def get_current_task(request: CustomRequest):
    """Retrieve a task."""

    current_task = Task.objects.filter(member=request.member, ended_at=None).last()

    if current_task is None:
        return JsonResponse({"message": "No task found"}, status=404)

    response = JsonResponse(current_task.to_dict(), status=200)
    response.set_cookie("auth_token", request.auth_token, httponly=True)

    return response


@router.put("/{task_id}", tags=["task"])
@login_token_required
def update_task(request: CustomRequest, task_id: str):
    """Update a task."""

    task = Task.objects.get(id=task_id)

    if request.member != task.member:
        return JsonResponse(
            {"message": "You are not allowed to access this task."}, status=403
        )

    task.ended_at = datetime.now(timezone.utc)
    task.save()

    response = JsonResponse(task.to_dict(), status=200)
    response.set_cookie("auth_token", request.auth_token, httponly=True)

    return response


@router.delete("/{task_id}", tags=["task"])
@login_token_required
def delete_task(request: CustomRequest, task_id: str):
    """Delete a task."""

    task = Task.objects.get(id=task_id)
    if request.member != task.member:
        return JsonResponse(
            {"message": "You are not allowed to access this task."}, status=403
        )

    task.delete()

    response = JsonResponse({"message": "Task deleted"}, status=204)
    response.set_cookie("auth_token", request.auth_token, httponly=True)

    return response
