import uuid

from django.db import models


class Task(models.Model):
    """Model for the task table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_possible_task = models.ForeignKey(
        "PossibleTask", on_delete=models.CASCADE, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="tasks")

    @property
    def duration(self):
        """Calculate the duration of the task in seconds."""
        if not self.ended_at:
            return 0

        total_seconds = (self.ended_at - self.created_at).total_seconds()

        return total_seconds < 10_000

    def to_dict(self):
        return {
            "id": self.id,
            "related_possible_task": self.related_possible_task.id,
            "created_at": self.created_at,
            "ended_at": self.ended_at,
            "updated_at": self.updated_at,
            "member": self.member.id,
            "duration": self.duration,
        }

    class Meta:
        """Meta class for the Task model."""

        db_table = "task"
