import json

import pytest

from tasks_api.tests.factories import PossibleTaskFactory


@pytest.mark.parametrize(
    "invalid_family_name",
    [
        "a",
        "a" * 26,
    ],
)
@pytest.mark.django_db
def test_register_create_family_with_invalid_family_name(invalid_family_name, client):
    payload = {
        "family_name": invalid_family_name,
        "username": "valid_name",
        "password": "ValidPassword123*",
    }

    response = client.post(
        "/register_create",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid data"}


@pytest.mark.parametrize(
    "invalid_member_name",
    [
        "a",
        "a" * 26,
    ],
)
@pytest.mark.django_db
def test_register_create_family_with_invalid_member_name(invalid_member_name, client):
    payload = {
        "family_name": "valid name",
        "username": invalid_member_name,
        "password": "ValidPassword123*",
    }

    response = client.post(
        "/register_create",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid data"}


@pytest.mark.parametrize(
    "invalid_password",
    [
        "a",
        "azerty",
        "AZERTY",
        "azertyuioipoiopqidpoqsid",
        "AZERTYUIOPIPOIPOQSDPOQSID",
        "123456789",
        "123456789azerty",
        "aA1",
        "alkjhazdkljsASDKQSJFDKSLM",
        "1324564aadfsdsgsdgfs",
        "ALDFSJMGKLJS1654",
    ],
)
@pytest.mark.django_db
def test_register_create_family_with_invalid_password(invalid_password, client):
    payload = {
        "family_name": "valid_name",
        "username": "valid_name",
        "password": invalid_password,
    }

    response = client.post(
        "/register_create",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == {"message": "Invalid data"}


@pytest.mark.parametrize(
    "invalid_family_name", ["invalid_name_because_too_long", "a", "     a     "]
)
@pytest.mark.django_db
def test_update_family_with_invalid_name(invalid_family_name, client):
    payload = {
        "family_name": invalid_family_name,
    }

    response = client.put(
        "/api/family/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "invalid_member_name", ["invalid_name_because_too_long", "a", "     a     "]
)
def test_update_member_with_invalid_name(invalid_member_name, client):
    payload = {
        "member_name": invalid_member_name,
    }

    response = client.put(
        "/api/member/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "invalid_p_task_name",
    [
        "T",
        "T" * 14,
    ],
)
def test_create_possible_task_with_invalid_name(invalid_p_task_name, client):
    payload = {
        "possible_task_name": invalid_p_task_name,
        "description": "valid description",
    }

    response = client.post(
        "/api/possible_task/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "invalid_p_task_name",
    [
        "T",
        "T" * 14,
    ],
)
@pytest.mark.django_db
def test_update_possible_task_with_invalid_name(invalid_p_task_name, client):
    p_task_to_modify = PossibleTaskFactory()

    payload = {
        "possible_task_name": invalid_p_task_name,
        "description": "valid description",
    }

    response = client.put(
        f"/api/possible_task/{p_task_to_modify.id}",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 422
