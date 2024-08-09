import uuid

from django.db import models

from emailmanager.crypto import decrypt
from TaskEqualizer.settings import MAX_LENGTH_USERNAME


class Member(models.Model):
    """Model for the member table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member_name = models.CharField(max_length=MAX_LENGTH_USERNAME, unique=True)
    email = models.EmailField(null=True, blank=True)
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
            "email": decrypt(self.email) or "",
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "family": self.family.id,
        }

    class Meta:
        """Meta class for the Member model."""

        db_table = "member"

    def get_email(self):
        if self.email is None:
            return None

        return decrypt(self.email)
