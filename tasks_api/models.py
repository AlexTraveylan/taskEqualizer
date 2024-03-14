import uuid

from django.db import models


class Family(models.Model):
    """Model for the family table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    family_name = models.CharField(max_length=100)
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
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="tasks")

    @property
    def duration(self):
        """Calculate the duration of the task in seconds."""
        total_seconds = (self.ended_at - self.created_at).total_seconds()

        # I supose that a task can't last more than 10_000 seconds
        return total_seconds if total_seconds < 10_000 else 0

    class Meta:
        """Meta class for the Task model."""

        db_table = "task"


class Invitation(models.Model):
    """Model for the invitation table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="invitations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta class for the Invitation model."""

        db_table = "invitation"
