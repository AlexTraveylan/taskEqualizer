import re

import pytest

from tasks_api.invitation.models import Invitation


@pytest.mark.django_db
def test_create_invitation(client, data_test):
    """Test the creation of an invitation code."""

    # We need to send the auth_token in the headers
    headers = {"Cookie": f"auth_token={data_test.token.to_jwt_token()}"}
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
