import json

import pytest
from django.utils import timezone

from tasks_api.ephemeral_task.models import EphemeralTask
from tasks_api.tests.factories import EphemeralTaskFactory, MemberFactory


@pytest.mark.django_db
def test_get_all_ephemeral_tasks_for_family(client, data_test):
    # should return tasks for the family of the user -> only 2 tasks
    EphemeralTaskFactory(family=data_test.family, member=data_test.member)
    EphemeralTaskFactory(family=data_test.family, member=data_test.member)
    EphemeralTaskFactory(member=MemberFactory(member_name="other_family_member"))

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.get(
        "/api/ephemeral_task/",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


@pytest.mark.django_db
def test_create_ephemeral_task(client, data_test):
    """Test the retrieval of a task."""

    payload = {
        "ephemeral_task_name": "Test Ephemeral Task",
        "description": "Ephemeral Task description",
        "value": 5,
    }

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.post(
        "/api/ephemeral_task/",
        data=json.dumps(payload),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["ephemeral_task_name"] == "Test Ephemeral Task"


@pytest.mark.django_db
def test_update_ephemeral_task(client, data_test):
    e_task = EphemeralTaskFactory(family=data_test.family, member=None)

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.put(
        f"/api/ephemeral_task/{e_task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["member"] == str(data_test.member.id)
    assert data["ended_at"] is not None


@pytest.mark.django_db
def test_update_ephemeral_task_when_task_is_already_done(client, data_test):
    e_task = EphemeralTaskFactory(
        family=data_test.family,
        member=data_test.member,
        ended_at=timezone.now(),
    )

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.put(
        f"/api/ephemeral_task/{e_task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_ephemeral_task(client, data_test):
    e_task = EphemeralTaskFactory(family=data_test.family, member=None)

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.delete(
        f"/api/ephemeral_task/{e_task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 200

    # Check if the e_task has been deleted
    e_tasks = EphemeralTask.objects.all()

    assert len(e_tasks) == 0


@pytest.mark.django_db
def test_delete_ephemeral_task_when_task_is_already_done(client, data_test):
    e_task = EphemeralTaskFactory(family=data_test.family, member=data_test.member)

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.delete(
        f"/api/ephemeral_task/{e_task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_ephemeral_task_when_other_family(client, data_test):
    e_task = EphemeralTaskFactory(member=None)

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.delete(
        f"/api/ephemeral_task/{e_task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 403
