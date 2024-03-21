import json

import pytest


@pytest.mark.django_db
def test_integr_register_create_family(client):

    body = {
        "family_name": "Test Family",
        "username": "test_user",
        "password": "test_password",
    }

    response = client.post(
        "/register_create", data=json.dumps(body), content_type="application/json"
    )

    assert response.status_code == 201
    assert response.cookies["auth_token"] is not None


@pytest.mark.django_db
def test_integr_login(client):

    register_body = {
        "family_name": "Test Family",
        "username": "test_user",
        "password": "test_password",
    }

    response_register = client.post(
        "/register_create",
        data=json.dumps(register_body),
        content_type="application/json",
    )

    assert response_register.status_code == 201

    login_body = {"username": "test_user", "password": "test_password"}

    response_login = client.post(
        "/login", data=json.dumps(login_body), content_type="application/json"
    )

    assert response_login.status_code == 200
    assert response_login.cookies["auth_token"] is not None
