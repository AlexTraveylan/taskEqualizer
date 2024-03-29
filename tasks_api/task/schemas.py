from ninja import Schema
from ninja.orm import create_schema

from tasks_api.task.models import Task


class TaskSchemaIn(Schema):
    related_possible_task_id: str


TaskSchemaOut = create_schema(Task)
