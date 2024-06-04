import json

import pytest

from tasks_api.models import Task


@pytest.mark.django_db
def test_create_task(client, data_test):
    """Test the creation of an invitation code."""

    payload = {"related_possible_task_id": str(data_test.possible_task.id)}

    # We need to send the auth_token in the headers
    headers = {
        "Cookie": f"auth_token={data_test.token.to_jwt_token()}",
    }
    response = client.post(
        "/api/task/",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 201

    # Check if the task has been created
    task = Task.objects.all()

    assert len(task) == 2
    assert task[1].related_possible_task_id == data_test.possible_task.id
    assert task[1].member_id == data_test.member.id


@pytest.mark.django_db
def test_retrieve_task(client, data_test):
    """Test the retrieval of a task."""

    # We need to send the auth_token in the headers
    headers = {
        "Cookie": f"auth_token={data_test.token.to_jwt_token()}",
    }
    response = client.get(
        "/api/task/",
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == str(data_test.task.id)
    assert response_data["related_possible_task"] == str(data_test.possible_task.id)
    assert response_data["member"] == str(data_test.member.id)


@pytest.mark.django_db
def test_update_task(client, data_test):
    """Test the update of a task."""

    payload = {"ended_at": "2021-01-01T00:00:00Z"}

    # We need to send the auth_token in the headers
    headers = {
        "Cookie": f"auth_token={data_test.token.to_jwt_token()}",
    }
    response = client.put(
        f"/api/task/{data_test.task.id}",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 200

    # Check if the task has been updated
    task = Task.objects.get(id=data_test.task.id)

    assert task.ended_at != 0


@pytest.mark.django_db
def test_delete_task(client, data_test):
    """Test the deletion of a task."""

    # We need to send the auth_token in the headers
    headers = {
        "Cookie": f"auth_token={data_test.token.to_jwt_token()}",
    }
    response = client.delete(
        f"/api/task/{data_test.task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 204

    # Check if the task has been deleted
    task = Task.objects.all()

    assert len(task) == 0
