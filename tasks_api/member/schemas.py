from ninja import Schema
from ninja.orm import create_schema

from tasks_api.member.models import Member


class MemberSchemaIn(Schema):
    member_name: str
    family_id: int


MemberSchemaOut = create_schema(Member)
