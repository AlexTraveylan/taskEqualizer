import uuid

from django.db import models


class Family(models.Model):
    """Model for the family table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    family_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.family_name)

    class Meta:
        """Meta class for the Family model."""

        db_table = "family"


class Member(models.Model):
    """Model for the member table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="members"
    )

    def __str__(self):
        return str(self.member_name)

    class Meta:
        """Meta class for the Member model."""

        db_table = "member"


class PossibleTask(models.Model):
    """Model for the possible_task table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class Task(models.Model):
    """Model for the task table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
