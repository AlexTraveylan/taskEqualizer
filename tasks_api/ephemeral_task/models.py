import uuid

from django.db import models


class ValueChoices(models.IntegerChoices):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 5
    LEVEL_4 = 10
    LEVEL_5 = 15
    LEVEL_6 = 30
    LEVEL_7 = 60
    LEVEL_8 = 120


class EphemeralTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ephemeral_task_name = models.CharField(max_length=25)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(choices=ValueChoices.choices)
    ended_at = models.DateTimeField(null=True, blank=True)
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="ephemeral_task"
    )
    member = models.ForeignKey(
        "Member",
        on_delete=models.CASCADE,
        related_name="ephemeral_task",
        null=True,
        default=None,
    )

    def __str__(self):
        return str(self.ephemeral_task_name)

    def to_dict(self):
        return {
            "id": self.id,
            "ephemeral_task_name": self.ephemeral_task_name,
            "description": self.description,
            "created_at": self.created_at,
            "value": self.value,
            "ended_at": self.ended_at,
            "family": self.family.id,
            "member": self.member.id if self.member else None,
        }

    def to_taks_like_dict(self):
        return {
            "id": self.id,
            "related_possible_task": "ephemeral_task",
            "created_at": self.created_at,
            "ended_at": self.ended_at,
            "updated_at": self.ended_at,
            "member": self.member.id,
            "duration": self.value * 60,
        }

    class Meta:
        db_table = "ephemeral_task"
