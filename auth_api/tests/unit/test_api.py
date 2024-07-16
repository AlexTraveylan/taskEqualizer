import json
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth.models import User

from auth_api.views import login, register_create_family
from TaskEqualizer.settings import TOKEN_NAME
from tasks_api.family.models import Family
from tasks_api.member.models import Member


@pytest.fixture
@pytest.mark.django_db
def setup_login_test():
    user = User.objects.create(username="testuser")
    family = Family.objects.create(family_name="testfamily")
    member = Member.objects.create(member_name="testuser", family=family)
    return user, member


@patch("auth_api.views.authenticate")
@pytest.mark.django_db
def test_login_success(mock_authenticate, setup_login_test):
    user, _ = setup_login_test
    mock_authenticate.return_value = user

    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps({"username": "testuser", "password": "ValidPassword123*"})

    response = login(request)

    assert response.status_code == 200

    json_data = json.loads(response.content)

    assert TOKEN_NAME in json_data
    assert json_data["message"] == "Login successful"


@patch("auth_api.views.authenticate")
@pytest.mark.django_db
def test_login_fail(mock_authenticate, setup_login_test):
    mock_authenticate.return_value = None

    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps({"username": "testuser", "password": "wrong_password"})

    response = login(request)

    assert response.status_code == 401

    content_str = response.content.decode("utf-8")
    json_data = json.loads(content_str)

    assert json_data["message"] == "Invalid credentials"


@pytest.mark.django_db
def test_register_succes():
    User.objects.create(username="testuser")

    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps(
        {
            "family_name": "testfamily",
            "username": "newuser",
            "password": "ValidPassword123*",
        }
    )

    response = register_create_family(request)

    assert response.status_code == 201

    json_data = json.loads(response.content)

    assert TOKEN_NAME in json_data
    assert json_data["message"] == "User created"


@pytest.mark.django_db
def test_register_fail_missing_informations():
    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps(
        {
            "family_name": "testfamily",
            "username": "newuser",
        }
    )

    response = register_create_family(request)

    assert response.status_code == 400

    content_str = response.content.decode("utf-8")
    json_data = json.loads(content_str)

    assert json_data["message"] == "Invalid data"


@pytest.mark.django_db
def test_register_fail_user_already_exist():
    User.objects.create(username="testuser")

    request = MagicMock()
    request.method = "POST"
    request.body = json.dumps(
        {
            "family_name": "testfamily",
            "username": "testuser",
            "password": "ValidPassword123*",
        }
    )

    response = register_create_family(request)

    assert response.status_code == 400

    content_str = response.content.decode("utf-8")
    json_data = json.loads(content_str)

    assert json_data["message"] == "Username already exists"
