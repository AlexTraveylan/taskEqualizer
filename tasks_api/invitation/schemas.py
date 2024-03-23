from datetime import datetime

from pydantic import BaseModel, Field

from tasks_api.family.models import Family


class InvitationCreate(BaseModel):
    """Schema for creating an invitation."""

    code: str = Field(min_length=8, max_length=8, pattern="^[A-Z0-9]*$")
    family: Family
    expired_at: datetime

    def to_dict(self):
        return {
            "code": self.code,
            "family": self.family.id,
            "expired_at": self.expired_at,
        }
