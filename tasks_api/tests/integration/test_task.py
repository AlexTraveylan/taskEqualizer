import json
import time
from uuid import UUID

import pytest
from django.utils import timezone

from tasks_api.models import Task


@pytest.mark.django_db
def test_create_task(client, data_test):
    """Test the creation of an invitation code."""

    payload = {"related_possible_task_id": str(data_test.possible_task.id)}

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
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
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    time.sleep(0.1)
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

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    time.sleep(0.1)

    response = client.put(
        f"/api/task/{data_test.task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 200

    # Check if the task has been updated
    task = Task.objects.get(id=data_test.task.id)

    assert task.ended_at != 0
    assert task.duration_in_seconds == 1


@pytest.mark.django_db
def test_delete_task(client, data_test):
    """Test the deletion of a task."""

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.delete(
        f"/api/task/{data_test.task.id}",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 204

    # Check if the task has been deleted
    task = Task.objects.all()

    assert len(task) == 0


@pytest.mark.django_db
def test_clean_tasks(client, data_test):
    """Test the cleaning of tasks."""

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    time.sleep(0.1)

    # data_test.task should not be deleted

    # should be deleted, task forgotten
    task_1 = Task.objects.create(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        related_possible_task=data_test.possible_task,
        member=data_test.member,
        ended_at=None,
        duration_in_seconds=0,
    )
    task_1.created_at = timezone.now() - timezone.timedelta(days=5)
    task_1.save()

    # should not be deleted, task in duration
    task_2 = Task.objects.create(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        related_possible_task=data_test.possible_task,
        member=data_test.member,
        ended_at=timezone.now()
        - timezone.timedelta(days=5)
        + timezone.timedelta(hours=1),
        duration_in_seconds=3600,  # <2h
    )
    task_2.created_at = timezone.now() - timezone.timedelta(days=5)
    task_2.save()

    # should be deleted, task to long
    task_3 = Task.objects.create(
        id=UUID("00000000-0000-0000-0000-000000000003"),
        related_possible_task=data_test.possible_task,
        member=data_test.member,
        ended_at=timezone.now() - timezone.timedelta(days=3),
        duration_in_seconds=0,
    )
    task_3.created_at = timezone.now() - timezone.timedelta(days=5)
    task_3.save()

    response = client.delete(
        "/api/task/clean",
        headers=headers,
        content_type="application/json",
    )

    assert response.status_code == 204

    # Check if the task has been deleted
    tasks = Task.objects.all()
    assert len(tasks) == 2
