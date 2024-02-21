"""This module contains the views for the tasks_api app."""

from ninja import NinjaAPI

from tasks_api.CRUDs.family.api import router as family_router
from tasks_api.CRUDs.member.api import router as member_router
from tasks_api.CRUDs.possibles_tasks.api import router as possible_task_router
from tasks_api.CRUDs.task.api import router as task_router

api = NinjaAPI()

api.add_router("family", family_router)
api.add_router("member", member_router)
api.add_router("possible_task", possible_task_router)
api.add_router("task", task_router)
