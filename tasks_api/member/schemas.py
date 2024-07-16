from ninja import Schema
from ninja.orm import create_schema
from pydantic import field_validator

from auth_api.schemas import validate_username
from tasks_api.member.models import Member


class MemberSchemaIn(Schema):
    member_name: str

    @field_validator("member_name")
    def validate_member_name(cls, value: str) -> str:
        return validate_username(value)


MemberSchemaOut = create_schema(Member)
