from ninja import Schema
from ninja.orm import create_schema
from pydantic import field_validator

from tasks_api.possibles_task.models import PossibleTask
from tasks_api.validators import validate_task_name


class PossibleTaskSchemaIn(Schema):
    possible_task_name: str
    description: str

    @field_validator("possible_task_name")
    def validate_possible_task_name(cls, value):
        return validate_task_name(value)

    @field_validator("description")
    def validate_description(cls, value):
        value = value.strip()

        if len(value) > 1000:
            raise ValueError("Description must be at most 1000 characters long")

        return value


PossibleTaskSchemaOut = create_schema(PossibleTask)
