import uuid

from django.db import models

from TaskEqualizer.settings import MAX_LENGTH_FAMILY_NAME


class Family(models.Model):
    """Model for the family table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    family_name = models.CharField(max_length=MAX_LENGTH_FAMILY_NAME)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.family_name)

    def to_dict(self):
        return {
            "id": self.id,
            "family_name": self.family_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    class Meta:
        """Meta class for the Family model."""

        db_table = "family"
