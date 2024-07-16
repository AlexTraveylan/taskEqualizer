from datetime import datetime

from pydantic import BaseModel, field_validator

from auth_api.validators import validate_invitation_code
from tasks_api.family.models import Family


class InvitationCreate(BaseModel):
    """Schema for creating an invitation."""

    code: str
    family: Family
    expired_at: datetime

    @field_validator("code")
    def code_length(cls, value: str) -> str:
        return validate_invitation_code(value)

    def to_dict(self):
        return {
            "code": self.code,
            "family": self.family.id,
            "expired_at": self.expired_at,
        }
