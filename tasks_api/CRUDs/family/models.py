from django.db import models
from ninja.orm import create_schema

from TaskEqualizer.settings import STANDARD_EXCLUDE


class Family(models.Model):
    """Model for the family table."""

    family_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.family_name)

    class Meta:
        """Meta class for the Family model."""

        db_table = "family"


FamilySchemaIn = create_schema(Family, exclude=STANDARD_EXCLUDE)
FamilySchemaOut = create_schema(Family)
