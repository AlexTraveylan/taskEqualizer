import math
import uuid
from datetime import date

from django.db import models
from django.utils import timezone

from TaskEqualizer.settings import MAX_SECOND_FOR_TASK


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
    duration_in_seconds = models.IntegerField(default=0)

    def duration(self, until: date) -> int:
        """Return the duration of the task in seconds from the creation to a given date."""
        if not until:
            return 0

        total_seconds = (until - self.created_at).total_seconds()

        if total_seconds > MAX_SECOND_FOR_TASK:  # 2h
            return 0

        return math.ceil(total_seconds)

    def to_dict(self):
        return {
            "id": self.id,
            "related_possible_task": self.related_possible_task.id,
            "created_at": self.created_at,
            "ended_at": self.ended_at,
            "updated_at": self.updated_at,
            "member": self.member.id,
            "duration": self.duration_in_seconds,
        }

    def __str__(self):
        return ", ".join([f"{key}={value}" for key, value in self.to_dict().items()])

    def is_not_current(self) -> bool:
        date_now = timezone.now()
        return self.ended_at is None and self.duration(date_now) == 0

    def is_invalid(self) -> bool:
        return self.ended_at is not None and self.duration_in_seconds == 0

    class Meta:
        """Meta class for the Task model."""

        db_table = "task"
