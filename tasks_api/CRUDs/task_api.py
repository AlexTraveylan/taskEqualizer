from ninja import Router

from tasks_api.models import Task
from tasks_api.schemas import TaskSchemaIn, TaskSchemaOut

router = Router()


@router.post("/", response=TaskSchemaOut, tags=["task"])
def create_task(request, payload: TaskSchemaIn):
    """Create a task."""

    new_task = Task.objects.create(**payload.dict())

    return new_task


@router.get("/", response=list[TaskSchemaOut], tags=["task"])
def list_tasks(request):
    """List all tasks."""
    tasks = Task.objects.all()

    return tasks


@router.get("/{task_id}", response=TaskSchemaOut, tags=["task"])
def retrieve_task(request, task_id: int):
    """Retrieve a task."""

    task = Task.objects.get(id=task_id)

    return task


@router.put("/{task_id}", response=TaskSchemaOut, tags=["task"])
def update_task(request, task_id: int, payload: TaskSchemaIn):
    """Update a task."""

    task = Task.objects.get(id=task_id)

    for key, value in payload.dict().items():
        setattr(task, key, value)

    task.save()

    return task


@router.delete("/{task_id}", response=TaskSchemaOut, tags=["task"])
def delete_task(request, task_id: int):
    """Delete a task."""

    task = Task.objects.get(id=task_id)
    task.delete()

    return task
