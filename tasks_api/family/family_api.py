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

    response = JsonResponse(members_dict, safe=False, status=200)

    return response


@router.get("/possible_tasks/", tags=["family"])
@login_token_required
def list_possibles_tasks_by_family(request: CustomRequest):
    """List all possible tasks by family."""

    possible_tasks = request.member.family.possible_tasks.all()
    possible_tasks_dict = list(possible_tasks.values())

    return JsonResponse(possible_tasks_dict, safe=False, status=200)


@router.get("/", tags=["family"])
@login_token_required
def retrieve_family(request: CustomRequest):
    """Retrieve a family."""

    return JsonResponse(request.member.family.to_dict(), status=200)


@router.get("/tasks/", tags=["family"])
@login_token_required
def get_tasks_by_members(request: CustomRequest):
    """Get tasks by members."""

    members = request.member.family.members.all()

    return JsonResponse(
        {
            "data": [
                {
                    "member_name": member.member_name,
                    "tasks": [task.to_dict() for task in member.tasks.all()],
                }
                for member in members
            ]
        },
        status=200,
    )


@router.get("/possibles_taks_details/", tags=["family"])
@login_token_required
def get_possibles_tasks_details(request: CustomRequest):
    """Get possibles tasks details."""

    possible_tasks = request.member.family.possible_tasks.all()
    members = request.member.family.members.all()
    tasks = {member: member.tasks.all() for member in members}

    data = [
        {
            "p_task_id": p_task.id,
            "members": [
                {
                    "member_name": member.member_name,
                    "tasks": [
                        task.to_dict()
                        for task in tasks[member]
                        if task.related_possible_task == p_task
                    ],
                }
                for member in members
            ],
        }
        for p_task in possible_tasks
    ]

    return JsonResponse({"data": data}, status=200)


@router.put("/", tags=["family"])
@login_token_required
def update_family(request: CustomRequest, payload: FamilySchemaIn):
    """Update a family."""

    family = request.member.family

    family.family_name = payload.family_name

    family.save()

    return JsonResponse({"message": "Family updated successfully."}, status=200)


@router.delete("/", tags=["family"])
@login_token_required
def delete_family(request: CustomRequest):
    """Delete a family."""

    request.member.family.delete()

    response = JsonResponse({"message": "Family deleted successfully."}, status=204)
    response.cookies.clear()

    return response
