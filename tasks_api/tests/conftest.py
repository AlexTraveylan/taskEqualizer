from dataclasses import dataclass

import pytest

from auth_api.auth_token import HeaderJwtToken
from tasks_api.models import Family, Member, PossibleTask, Task
from tasks_api.tests.factories import (
    FamilyFactory,
    FamilySettingsFactory,
    MemberFactory,
    PossibleTaskFactory,
)


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
    family = FamilyFactory()
    FamilySettingsFactory(family=family)
    member = MemberFactory(family=family)
    p_task = PossibleTaskFactory(family=family)
    task = Task.objects.create(related_possible_task=p_task, member=member)
    token = HeaderJwtToken(member.id)

    return DataTest(family, member, token, p_task, task)
