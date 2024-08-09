import json

import pytest
from django.utils import timezone

from TaskEqualizer.settings import TOKEN_NAME
from tasks_api.models import Family, Invitation


@pytest.mark.django_db
def test_integr_register_create_family(client):
    body = {
        "family_name": "Test Family",
        "username": "test_user",
        "password": "ValidPassword123*",
        "locale": "en",
    }

    response = client.post(
        "/register_create", data=json.dumps(body), content_type="application/json"
    )

    assert response.status_code == 201
    assert response.json()[TOKEN_NAME] is not None


@pytest.mark.django_db
def test_integr_login(client):
    register_body = {
        "family_name": "Test Family",
        "username": "test_user",
        "password": "ValidPassword123*",
        "locale": "en",
    }

    response_register = client.post(
        "/register_create",
        data=json.dumps(register_body),
        content_type="application/json",
    )

    assert response_register.status_code == 201

    login_body = {"username": "test_user", "password": "ValidPassword123*"}

    response_login = client.post(
        "/login", data=json.dumps(login_body), content_type="application/json"
    )

    assert response_login.status_code == 200
    assert response_login.json()[TOKEN_NAME] is not None


@pytest.mark.django_db
def test_integr_register_with_invitation(client):
    """Test if a user can register with an invitation code."""

    # Create a family and an invitation
    family = Family.objects.create(family_name="Test Family")
    Invitation.objects.create(
        family=family,
        code="TESTCODE",
        expired_at=timezone.now() + timezone.timedelta(days=1),
    )

    # Register a user with the invitation
    payload = {
        "username": "test_user",
        "password": "ValidPassword123*",
        "invitation_code": "TESTCODE",
    }
    response = client.post(
        "/register_invite", data=json.dumps(payload), content_type="application/json"
    )

    # Check if the user is created and logged in
    assert response.status_code == 201
    assert response.json()[TOKEN_NAME] is not None

    # Check if the user is in the family
    member = family.members.first()
    assert member.member_name == "test_user"

    # Check if the invitation is used
    invitation = Invitation.objects.get(code="TESTCODE")
    assert invitation.is_used is True
