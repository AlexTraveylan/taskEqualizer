import json

import pytest

from tasks_api.models import Family, Member, PossibleTask, Task


@pytest.mark.django_db
def test_list_members_by_family(client, data_test):
    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/members/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1
    assert body_response[0]["id"] == str(data_test.member.id)


@pytest.mark.django_db
def test_list_members_by_family_with_two_members(client, data_test):
    new_member = Member.objects.create(
        member_name="Test Member 2", family=data_test.family
    )

    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/members/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 2
    assert body_response[0]["id"] == str(data_test.member.id)
    assert body_response[1]["id"] == str(new_member.id)


@pytest.mark.django_db
def test_list_possibles_tasks_by_family(client, data_test):
    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/possible_tasks/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1
    assert body_response[0]["id"] == str(data_test.possible_task.id)


@pytest.mark.django_db
def test_list_possibles_tasks_by_family_with_two_possible_tasks(client, data_test):
    new_possible_task = PossibleTask.objects.create(
        possible_task_name="Test Task 2",
        description="Task created for tests",
        family=data_test.family,
    )

    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/possible_tasks/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 2
    assert body_response[0]["id"] == str(data_test.possible_task.id)
    assert body_response[1]["id"] == str(new_possible_task.id)


@pytest.mark.django_db
def test_update_family(client, data_test):
    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}

    payload = {"family_name": "New Family Name"}

    response = client.put("/api/family/", data=json.dumps(payload), headers=headers)

    assert response.status_code == 200

    family = Family.objects.get(id=data_test.family.id)

    assert family.family_name == "New Family Name"


@pytest.mark.django_db
def test_delete_family(client, data_test):
    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}

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
def test_get_tasks_by_members(client, data_test):
    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}

    response = client.get("/api/family/tasks/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1
    assert body_response["data"][0]["member_name"] == data_test.member.member_name
    assert body_response["data"][0]["tasks"][0]["id"] == str(data_test.task.id)
