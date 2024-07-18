import re

import pytest
from django.utils import timezone

from tasks_api.invitation.models import Invitation
from tasks_api.tests.factories import InvitationFactory


@pytest.mark.django_db
def test_create_invitation(client, data_test):
    """Test the creation of an invitation code."""

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.get("/api/invitation/", headers=headers)

    assert response.status_code == 201

    # We check that the code is send back
    body_response = response.json()
    code = body_response["code"]

    assert len(code) == 8
    assert re.match("^[A-Z0-9]*$", code)

    # We check that the code is in the database
    invitation = Invitation.objects.filter(code=code).first()

    assert invitation.family == data_test.family
    assert invitation.expired_at is not None
    assert invitation.is_used is False


@pytest.mark.django_db
def test_get_valid_invitation_list(client, data_test):
    """Test the retrieval of valid invitation codes."""

    InvitationFactory(
        family=data_test.family, expired_at=timezone.now() - timezone.timedelta(days=1)
    )
    valid_code = InvitationFactory(
        family=data_test.family, expired_at=timezone.now() + timezone.timedelta(days=1)
    )

    InvitationFactory(expired_at=timezone.now() + timezone.timedelta(days=1))

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.get("/api/invitation/get_valid_list/", headers=headers)

    assert response.status_code == 200

    # We check that the code is send back
    body_response = response.json()
    assert len(body_response["data"]) == 1
    assert body_response["data"][0]["id"] == str(valid_code.id)
