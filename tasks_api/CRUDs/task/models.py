from django.db import models
from ninja import Schema
from ninja.orm import create_schema


class Task(models.Model):
    """Model for the task table."""

    related_possible_task = models.ForeignKey(
        "PossibleTask", on_delete=models.CASCADE, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        """Meta class for the Task model."""

        db_table = "task"


TaskSchemaIn = create_schema(Task, fields=["related_possible_task", "member"])


class TaskSchemaIn(Schema):
    related_possible_task_id: int
    member_id: int


TaskSchemaOut = create_schema(Task)
