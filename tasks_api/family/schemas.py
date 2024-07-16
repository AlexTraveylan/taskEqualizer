from ninja import Schema
from ninja.orm import create_schema
from pydantic import field_validator

from auth_api.schemas import validate_family_name
from tasks_api.family.models import Family

FamilySchemaOut = create_schema(Family)


class FamilySchemaIn(Schema):
    family_name: str

    @field_validator("family_name")
    def validate_family_name(cls, value: str) -> str:
        return validate_family_name(value)
