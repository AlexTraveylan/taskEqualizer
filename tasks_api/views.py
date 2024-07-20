"""This module contains the views for the tasks_api app."""

from ninja import NinjaAPI

from tasks_api.ephemeral_task.ephemeral_task_api import router as ephemeral_task_router
from tasks_api.family.family_api import router as family_router
from tasks_api.invitation.invitation_api import router as invitation_router
from tasks_api.member.member_api import router as member_router
from tasks_api.possibles_task.possibles_tasks_api import router as possible_task_router
from tasks_api.task.task_api import router as task_router

api = NinjaAPI()

api.add_router("family", family_router)
api.add_router("member", member_router)
api.add_router("possible_task", possible_task_router)
api.add_router("task", task_router)
api.add_router("invitation", invitation_router)
api.add_router("invitation", ephemeral_task_router)
