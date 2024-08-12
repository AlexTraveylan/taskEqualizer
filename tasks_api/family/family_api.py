from collections import defaultdict
from datetime import date

from django.db.models.functions import TruncDay
from django.http import JsonResponse
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.ephemeral_task.models import EphemeralTask
from tasks_api.family.schemas import FamilySchemaIn
from tasks_api.task.models import Task

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

    rows = []
    for member in members:
        tasks = [task.to_dict() for task in member.tasks.all()]
        ephemeral_tasks = [
            ephemeral_task.to_tasks_like_dict()
            for ephemeral_task in member.ephemeral_task.all()
        ]

        rows.append(
            {
                "member_name": member.member_name,
                "tasks": tasks + ephemeral_tasks,
            }
        )

    return JsonResponse({"data": rows}, status=200)


@router.get("/possibles_taks_details/", tags=["family"])
@login_token_required
def get_possibles_tasks_details(request: CustomRequest):
    """Get possibles tasks details."""

    possible_tasks_id = [task.id for task in request.member.family.possible_tasks.all()]
    possible_tasks_id.append("ephemeral_task")
    members = request.member.family.members.all()

    tasks = {}
    for member in members:
        member_tasks = list(member.tasks.all())
        member_ephemeral_tasks = list(member.ephemeral_task.all())
        tasks[member] = member_tasks + member_ephemeral_tasks

    data = [
        {
            "p_task_id": p_task_id,
            "members": [
                {
                    "member_name": member.member_name,
                    "tasks": [
                        t_dict
                        for task in tasks[member]
                        if (t_dict := task.to_tasks_like_dict())[
                            "related_possible_task"
                        ]
                        == p_task_id
                    ],
                }
                for member in members
            ],
        }
        for p_task_id in possible_tasks_id
    ]

    return JsonResponse({"data": data}, status=200)


@router.get("/tasks_by_date_by_member/", tags=["family"])
@login_token_required
def get_tasks_by_date_by_member(request: CustomRequest):
    """Get tasks by date by member."""

    filtered_tasks = Task.objects.filter(
        duration_in_seconds__gt=0,
        member__family=request.member.family,
    ).prefetch_related("member")
    annotated_tasks = filtered_tasks.annotate(day=TruncDay("created_at"))

    tasks_by_day: dict[date, list[Task]] = defaultdict(list)
    for task in annotated_tasks:
        tasks_by_day[task.day].append(task)

    result: dict[date, dict[str, list[dict]]] = {}

    for day, tasks in tasks_by_day.items():
        day = day.strftime("%Y-%m-%d")

        for task in tasks:
            if day not in result:
                result[day] = defaultdict(list)

            result[day][task.member.member_name].append(
                {"duration": task.duration_in_seconds}
            )

    filtered_ephemeral_tasks = EphemeralTask.objects.filter(
        family=request.member.family,
        ended_at__isnull=False,
    ).prefetch_related("member")
    annotated_ephemeral_tasks = filtered_ephemeral_tasks.annotate(
        day=TruncDay("ended_at")
    )

    ephemeral_tasks_by_day: dict[date, list[EphemeralTask]] = defaultdict(list)
    for ephemeral_task in annotated_ephemeral_tasks:
        ephemeral_tasks_by_day[ephemeral_task.day].append(ephemeral_task)

    for day, ephemeral_tasks in ephemeral_tasks_by_day.items():
        day = day.strftime("%Y-%m-%d")

        for ephemeral_task in ephemeral_tasks:
            if day not in result:
                result[day] = defaultdict(list)

            result[day][ephemeral_task.member.member_name].append(
                {"duration": ephemeral_task.value * 60}
            )

    return JsonResponse(result, status=200)


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
