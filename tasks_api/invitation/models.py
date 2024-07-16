import uuid

from django.db import models


class Invitation(models.Model):
    """Model for the invitation table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=8)
    is_used = models.BooleanField(default=False)
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="invitations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "is_used": self.is_used,
            "family": self.family.id,
            "created_at": self.created_at,
            "expired_at": self.expired_at,
        }

    class Meta:
        """Meta class for the Invitation model."""

        db_table = "invitation"
