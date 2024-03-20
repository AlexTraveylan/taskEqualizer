import pytest

from tasks_api.models import Family, Member


@pytest.fixture
@pytest.mark.django_db
def family_for_test():

    family = Family.objects.create(family_name="Test Family")

    return family


@pytest.fixture
@pytest.mark.django_db
def member_for_test(family_for_test):

    member = Member.objects.create(member_name="Test Member", family=family_for_test)

    return member
