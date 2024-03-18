from django.http import HttpRequest, JsonResponse
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.task.models import Task
from tasks_api.task.schemas import TaskSchemaIn, TaskSchemaOut

router = Router()


@login_token_required
@router.post("/", tags=["task"])
def create_task(request: CustomRequest, payload: TaskSchemaIn):
    """Create a task."""

    if request.member.id != payload.member_id:
        return JsonResponse({"message": "Invalid member_id"}, status=400)

    new_task = Task.objects.create(**payload.dict())

    response = JsonResponse(new_task.dict(), status=201)
    response.set_cookie("auth_token", request.auth_token)

    return response


@router.get("/{task_id}", response=TaskSchemaOut, tags=["task"])
def retrieve_task(request: HttpRequest, task_id: int):
    """Retrieve a task."""

    task = Task.objects.get(id=task_id)

    return task


@login_token_required
@router.put("/{task_id}", tags=["task"])
def update_task(request: CustomRequest, task_id: int, payload: TaskSchemaIn):
    """Update a task."""

    task = Task.objects.get(id=task_id)

    if request.member != task.member:
        return JsonResponse(
            {"message": "You are not allowed to access this task."}, status=403
        )

    for key, value in payload.dict().items():
        setattr(task, key, value)

    task.save()

    response = JsonResponse(task.dict(), status=200)
    response.set_cookie("auth_token", request.auth_token)

    return response


@login_token_required
@router.delete("/{task_id}", tags=["task"])
def delete_task(request: CustomRequest, task_id: int):
    """Delete a task."""

    task = Task.objects.get(id=task_id)
    if request.member != task.member:
        return JsonResponse(
            {"message": "You are not allowed to access this task."}, status=403
        )

    task.delete()

    response = JsonResponse({"message": "Task deleted"}, status=200)
    response.set_cookie("auth_token", request.auth_token)

    return response
