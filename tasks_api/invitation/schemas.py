from ninja import Schema
from pydantic import field_validator

from tasks_api.validators import validate_email


class InvitationWithEmailIn(Schema):
    email: str

    @field_validator("email")
    def validate_email_field(cls, value: str) -> str:
        return validate_email(value)
