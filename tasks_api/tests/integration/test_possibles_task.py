import json

import pytest

from tasks_api.models import PossibleTask


@pytest.mark.django_db
def test_create_possible_task(client, data_test):
    """Test the creation of an invitation code."""

    payload = {
        "possible_task_name": "Test Task 2",
        "description": "This is a additional task.",
    }

    # We need to send the auth_token in the headers
    headers = {
        "Cookie": f"auth_token={data_test.token.to_jwt_token()}",
    }
    response = client.post(
        "/api/possible_task/",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 201

    # Check if the task has been created
    possibles_tasks = PossibleTask.objects.all()
    assert len(possibles_tasks) == 2


@pytest.mark.django_db
def test_update_possible_task(client, data_test):
    """Test the update of a possible task."""

    payload = {
        "possible_task_name": "Test Task modified",
        "description": "Task modified.",
    }

    # We need to send the auth_token in the headers
    headers = {
        "Cookie": f"auth_token={data_test.token.to_jwt_token()}",
    }
    response = client.put(
        f"/api/possible_task/{data_test.possible_task.id}",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 200

    # Check if the task has been updated
    possible_task = PossibleTask.objects.filter(
        possible_task_name="Test Task modified"
    ).first()
    assert possible_task.possible_task_name == "Test Task modified"


@pytest.mark.django_db
def test_delete_possible_task(client, data_test):
    """Test the deletion of a possible task."""

    # We need to send the auth_token in the headers
    headers = {
        "Cookie": f"auth_token={data_test.token.to_jwt_token()}",
    }
    response = client.delete(
        f"/api/possible_task/{data_test.possible_task.id}", headers=headers
    )

    assert response.status_code == 204

    # Check if the task has been deleted
    possibles_tasks = PossibleTask.objects.all()
    assert len(possibles_tasks) == 0
