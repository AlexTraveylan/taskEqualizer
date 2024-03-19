from ninja import Schema
from ninja.orm import create_schema

from tasks_api.possibles_task.models import PossibleTask


class PossibleTaskSchemaIn(Schema):
    possible_task_name: str
    description: str


PossibleTaskSchemaOut = create_schema(PossibleTask)
