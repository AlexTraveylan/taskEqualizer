from ninja.orm import create_schema
from pydantic import BaseModel, Field, field_validator

from auth_api.schemas import validate_username
from emailmanager.crypto import encrypt
from tasks_api.member.models import Member
from tasks_api.validators import validate_email


class MemberSchemaIn(BaseModel):
    member_name: str
    email: str | None = Field(default=None)

    @field_validator("member_name")
    def validate_member_name(cls, value: str) -> str:
        return validate_username(value)

    @field_validator("email")
    def validate_email_field(cls, value: str | None) -> str | None:
        if value is None:
            return value

        email = validate_email(value)

        return encrypt(email)


MemberSchemaOut = create_schema(Member)
