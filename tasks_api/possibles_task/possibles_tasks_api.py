from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.possibles_task.models import PossibleTask
from tasks_api.possibles_task.schemas import PossibleTaskSchemaIn

router = Router()


@router.post("/", tags=["possible_task"])
@login_token_required
def create_possible_task(request: CustomRequest, payload: PossibleTaskSchemaIn):
    """Create a possible task."""

    family_id = request.member.family.id

    new_possible_task = PossibleTask.objects.create(
        **payload.dict(), family_id=family_id
    )

    return JsonResponse(new_possible_task.to_dict(), status=201)


@router.put("/{possible_task_id}", tags=["possible_task"])
@login_token_required
def update_possible_task(
    request: CustomRequest, possible_task_id: str, payload: PossibleTaskSchemaIn
):
    """Update a possible task."""

    possible_task = get_object_or_404(PossibleTask, id=possible_task_id)

    if request.member.family != possible_task.family:
        return JsonResponse(
            {"message": "You are not allowed to access this family."}, status=403
        )

    for key, value in payload.dict().items():
        setattr(possible_task, key, value)

    possible_task.save()

    return JsonResponse(possible_task.to_dict(), status=200)


@router.delete("/{possible_task_id}", tags=["possible_task"])
@login_token_required
def delete_possible_task(request: CustomRequest, possible_task_id: str):
    """Delete a possible task."""
    possible_task = get_object_or_404(PossibleTask, id=possible_task_id)

    if request.member.family != possible_task.family:
        return JsonResponse(
            {"message": "You are not allowed to access this possible task."}, status=403
        )

    possible_task.delete()

    return JsonResponse({"message": "Possible task deleted successfully."}, status=204)
