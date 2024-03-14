from ninja import Schema
from ninja.orm import create_schema

from TaskEqualizer.settings import STANDARD_EXCLUDE
from tasks_api.models import Family, Member, PossibleTask, Task

FamilySchemaIn = create_schema(Family, exclude=STANDARD_EXCLUDE)
FamilySchemaOut = create_schema(Family)


class MemberSchemaIn(Schema):
    member_name: str
    email: str
    password: str
    family_id: int


MemberSchemaOut = create_schema(Member)


class PossibleTaskSchemaIn(Schema):
    possible_task_name: str
    description: str
    family_id: int


PossibleTaskSchemaOut = create_schema(PossibleTask)


class TaskSchemaIn(Schema):
    related_possible_task_id: int
    member_id: int


TaskSchemaOut = create_schema(Task)
