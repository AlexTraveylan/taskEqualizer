from ninja import Schema
from ninja.orm import create_schema
from pydantic import field_validator

from TaskEqualizer.settings import MAX_EPHERMERAL_TASK_NAME, MIN_EPHERMERAL_TASK_NAME
from tasks_api.ephemeral_task.models import EphemeralTask, ValueChoices


class EphemeralTaskIn(Schema):
    ephemeral_task_name: str
    description: str
    value: int

    @field_validator("value")
    def check_value(cls, value):
        if value not in ValueChoices.values:
            raise ValueError("Invalid value")

        return value

    @field_validator("description")
    def check_description(cls, value):
        value = value.strip()

        if len(value) > 1000:
            raise ValueError("Description must be at most 1000 characters long")

        return value

    @field_validator("ephemeral_task_name")
    def check_ephemeral_task_name(cls, value):
        value = value.strip()

        if len(value) < MIN_EPHERMERAL_TASK_NAME:
            raise ValueError(
                f"Ephemeral task name must be at least {MIN_EPHERMERAL_TASK_NAME} characters long"
            )

        if len(value) > MAX_EPHERMERAL_TASK_NAME:
            raise ValueError(
                f"Ephemeral task name must be at most {MAX_EPHERMERAL_TASK_NAME} characters long"
            )

        return value


PossibleTaskSchemaOut = create_schema(EphemeralTask)
