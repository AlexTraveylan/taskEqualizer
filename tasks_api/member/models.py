import uuid

from django.db import models


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

    def to_dict(self):
        return {
            "id": self.id,
            "member_name": self.member_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "family": self.family.id,
        }

    class Meta:
        """Meta class for the Member model."""

        db_table = "member"
