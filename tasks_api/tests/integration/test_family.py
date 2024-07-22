import json

import pytest
from django.utils import timezone

from tasks_api.models import Family, Member, PossibleTask, Task
from tasks_api.tests.conftest import DataTest
from tasks_api.tests.factories import EphemeralTaskFactory, MemberFactory, TaskFactory


@pytest.mark.django_db
def test_list_members_by_family(client, data_test: DataTest):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/members/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1
    assert body_response[0]["id"] == str(data_test.member.id)


@pytest.mark.django_db
def test_list_members_by_family_with_two_members(client, data_test: DataTest):
    new_member = Member.objects.create(
        member_name="Test Member 2", family=data_test.family
    )

    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/members/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 2
    assert body_response[0]["id"] == str(data_test.member.id)
    assert body_response[1]["id"] == str(new_member.id)


@pytest.mark.django_db
def test_list_possibles_tasks_by_family(client, data_test: DataTest):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/possible_tasks/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1
    assert body_response[0]["id"] == str(data_test.possible_task.id)


@pytest.mark.django_db
def test_list_possibles_tasks_by_family_with_two_possible_tasks(
    client, data_test: DataTest
):
    new_possible_task = PossibleTask.objects.create(
        possible_task_name="Test Task 2",
        description="Task created for tests",
        family=data_test.family,
    )

    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/possible_tasks/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 2
    assert body_response[0]["id"] == str(data_test.possible_task.id)
    assert body_response[1]["id"] == str(new_possible_task.id)


@pytest.mark.django_db
def test_update_family(client, data_test: DataTest):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    payload = {"family_name": "New Family Name"}

    response = client.put("/api/family/", data=json.dumps(payload), headers=headers)

    assert response.status_code == 200

    family = Family.objects.get(id=data_test.family.id)

    assert family.family_name == "New Family Name"


@pytest.mark.django_db
def test_delete_family(client, data_test: DataTest):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.delete("/api/family/", headers=headers)

    assert response.status_code == 204

    family = Family.objects.filter(id=data_test.family.id).first()
    member = Member.objects.filter(id=data_test.member.id).first()
    possible_task = PossibleTask.objects.filter(id=data_test.possible_task.id).first()
    task = Task.objects.filter(id=data_test.task.id).first()

    assert len(response.cookies) == 0
    assert family is None
    assert member is None
    assert possible_task is None
    assert task is None


@pytest.mark.django_db
def test_get_tasks_by_members(client, data_test: DataTest):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/tasks/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1
    assert body_response["data"][0]["member_name"] == data_test.member.member_name
    assert body_response["data"][0]["tasks"][0]["id"] == str(data_test.task.id)


@pytest.mark.django_db
def test_get_possibles_tasks_details(client, data_test: DataTest):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/possibles_taks_details/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1


@pytest.mark.django_db
def test_get_tasks_by_date_by_member(client, data_test: DataTest):
    second_member = MemberFactory(family=data_test.family, member_name="Test Member 2")
    member_out_of_family = MemberFactory(member_name="Test Member 3")

    date_1 = timezone.now()
    date_2 = timezone.now() - timezone.timedelta(days=1)

    # Should be considered for date_1 and member 1
    task_1 = TaskFactory(member=data_test.member, duration_in_seconds=10)
    task_1.created_at = date_1
    task_1.save()

    # Should be considered for date_1 and member 1
    task_2 = TaskFactory(member=data_test.member, duration_in_seconds=20)
    task_2.created_at = date_1
    task_2.save()

    # Should be considered for date_2 and member 1
    task_3 = TaskFactory(member=data_test.member, duration_in_seconds=30)
    task_3.created_at = date_2
    task_3.save()

    # Should be considered for date_1 and member 2
    task_4 = TaskFactory(member=second_member, duration_in_seconds=40)
    task_4.created_at = date_1
    task_4.save()

    # Should be considered for date_2 and member 2
    task_5 = TaskFactory(member=second_member, duration_in_seconds=50)
    task_5.created_at = date_2
    task_5.save()

    # Should NOT be considered (member out of family)
    task_6 = TaskFactory(member=member_out_of_family, duration_in_seconds=60)
    task_6.created_at = date_1
    task_6.save()

    # Should be considered for date_1 and member 1
    EphemeralTaskFactory(
        family=data_test.family,
        member=data_test.member,
        ended_at=date_1,
    )

    # Should NOT be considered (member out of family)
    EphemeralTaskFactory(
        family=member_out_of_family.family,
        member=member_out_of_family,
        ended_at=date_1,
    )

    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/tasks_by_date_by_member/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    # 2 days populated
    assert len(body_response) == 2
    # 2 members for the first day
    assert len(body_response[date_1.strftime("%Y-%m-%d")]) == 2
    # 2 members for the second day
    assert len(body_response[date_2.strftime("%Y-%m-%d")]) == 2
    # 3 tasks for the first day and the first member
    assert (
        len(body_response[date_1.strftime("%Y-%m-%d")][data_test.member.member_name])
        == 3
    )
    # 1 task for the first day and the second member
    assert (
        len(body_response[date_1.strftime("%Y-%m-%d")][second_member.member_name]) == 1
    )
    # 1 task for the second day and the first member
    assert (
        len(body_response[date_2.strftime("%Y-%m-%d")][data_test.member.member_name])
        == 1
    )
    # 1 task for the second day and the second member
    assert (
        len(body_response[date_2.strftime("%Y-%m-%d")][second_member.member_name]) == 1
    )
