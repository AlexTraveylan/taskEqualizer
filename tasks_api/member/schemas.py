from ninja import Schema
from ninja.orm import create_schema

from tasks_api.member.models import Member


class MemberSchemaIn(Schema):
    member_name: str
    family_id: str


MemberSchemaOut = create_schema(Member)
