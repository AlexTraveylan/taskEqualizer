from django.shortcuts import get_object_or_404
from ninja import Router

from tasks_api.models import PossibleTask
from tasks_api.schemas import PossibleTaskSchemaIn, PossibleTaskSchemaOut

router = Router()


@router.post("/", response=PossibleTaskSchemaOut, tags=["possible_task"])
def create_possible_task(request, payload: PossibleTaskSchemaIn):
    """Create a possible task."""

    new_possible_task = PossibleTask.objects.create(**payload.dict())

    return new_possible_task


@router.get("/", response=list[PossibleTaskSchemaOut], tags=["possible_task"])
def list_possible_tasks(request):
    """List all possible tasks."""
    possible_tasks = PossibleTask.objects.all()

    return possible_tasks


@router.get(
    "/{possible_task_id}", response=PossibleTaskSchemaOut, tags=["possible_task"]
)
def retrieve_possible_task(request, possible_task_id: int):
    """Retrieve a possible task."""

    possible_task = get_object_or_404(PossibleTask, id=possible_task_id)

    return possible_task


@router.put(
    "/{possible_task_id}", response=PossibleTaskSchemaOut, tags=["possible_task"]
)
def update_possible_task(request, possible_task_id: int, payload: PossibleTaskSchemaIn):
    """Update a possible task."""

    possible_task = get_object_or_404(PossibleTask, id=possible_task_id)

    for key, value in payload.dict().items():
        setattr(possible_task, key, value)

    possible_task.save()

    return possible_task


@router.delete("/{possible_task_id}", tags=["possible_task"])
def delete_possible_task(request, possible_task_id: int):
    """Delete a possible task."""
    possible_task = get_object_or_404(PossibleTask, id=possible_task_id)
    possible_task.delete()

    return {"message": "Possible task deleted successfully."}
