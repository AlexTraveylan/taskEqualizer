from django.db import models
from ninja import Schema
from ninja.orm import create_schema


class PossibleTask(models.Model):
    """Model for the possible_task table."""

    possible_task_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="possible_tasks"
    )

    def __str__(self):
        return str(self.possible_task_name)

    class Meta:
        """Meta class for the PossibleTask model."""

        db_table = "possible_task"


class PossibleTaskSchemaIn(Schema):
    possible_task_name: str
    description: str
    family_id: int


PossibleTaskSchemaOut = create_schema(PossibleTask)
