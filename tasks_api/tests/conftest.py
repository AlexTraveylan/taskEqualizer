from dataclasses import dataclass

import pytest

from auth_api.auth_token import HeaderJwtToken
from tasks_api.models import Family, Member, PossibleTask, Task


@dataclass
class DataTest:
    family: Family
    member: Member
    token: HeaderJwtToken
    possible_task: PossibleTask
    task: Task


@pytest.fixture
@pytest.mark.django_db
def data_test():

    family = Family.objects.create(family_name="Test Family")
    member = Member.objects.create(member_name="Test Member", family=family)
    p_task = PossibleTask.objects.create(
        possible_task_name="Test Task",
        description="Task created for tests",
        family=family,
    )
    task = Task.objects.create(related_possible_task=p_task, member=member)
    token = HeaderJwtToken(member.id)

    return DataTest(family, member, token, p_task, task)
