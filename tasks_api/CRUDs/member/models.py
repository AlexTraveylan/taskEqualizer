from django.db import models
from ninja import Schema
from ninja.orm import create_schema


class Member(models.Model):
    """Model for the member table."""

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


class MemberSchemaIn(Schema):
    member_name: str
    email: str
    password: str
    family_id: int


MemberSchemaOut = create_schema(Member)
