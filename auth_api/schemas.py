from pydantic import BaseModel, field_validator

from auth_api.validators import (
    validate_family_name,
    validate_password,
    validate_username,
)
from TaskEqualizer.settings import INVITATION_CODE_SIZE


class RegisterCreateSchema(BaseModel):
    family_name: str
    username: str
    password: str

    @field_validator("family_name")
    def family_name_length(cls, value: str) -> str:
        return validate_family_name(value)

    @field_validator("username")
    def username_length(cls, value: str) -> str:
        return validate_username(value)

    @field_validator("password")
    def password_strength(cls, value: str) -> str:
        return validate_password(value)


class RegisterInviteSchema(BaseModel):
    username: str
    password: str
    invitation_code: str

    @field_validator("username")
    def username_length(cls, value: str) -> str:
        return validate_username(value)

    @field_validator("password")
    def password_strength(cls, value: str) -> str:
        return validate_password(value)

    @field_validator("invitation_code")
    def invitation_code_length(cls, value: str) -> str:
        if len(value) != INVITATION_CODE_SIZE:
            raise ValueError(
                f"Invitation code must be {INVITATION_CODE_SIZE} characters long"
            )

        return value.strip()
