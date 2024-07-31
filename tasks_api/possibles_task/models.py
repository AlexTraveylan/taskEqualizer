import uuid

from django.db import models


class PossibleTask(models.Model):
    """Model for the possible_task table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    possible_task_name = models.CharField(max_length=13)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="possible_tasks"
    )

    def __str__(self):
        return str(self.possible_task_name)

    def to_dict(self):
        return {
            "id": self.id,
            "possible_task_name": self.possible_task_name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "family_id": self.family.id,
        }

    class Meta:
        """Meta class for the PossibleTask model."""

        db_table = "possible_task"
