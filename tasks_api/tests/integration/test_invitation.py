import re

import pytest
from django.utils import timezone

from tasks_api.family_settings.models import FamilySettings
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


@pytest.mark.django_db
def test_delete_invitation(client, data_test):
    """Test the deletion of an invitation code."""

    invitation = InvitationFactory(family=data_test.family)

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.delete(f"/api/invitation/{invitation.id}", headers=headers)

    assert response.status_code == 200

    # We check that the code is in the database
    invitation = Invitation.objects.filter(id=invitation.id).first()

    assert invitation is None


@pytest.mark.django_db
def test_clean_invitations(client, data_test):
    """Test the deletion of expired and unused invitations."""

    should_be_deleted_cause_perimed = InvitationFactory(
        family=data_test.family, expired_at=timezone.now() - timezone.timedelta(days=1)
    )
    should_not_be_deleted_cause_active = InvitationFactory(
        family=data_test.family, expired_at=timezone.now() + timezone.timedelta(days=1)
    )
    should_not_be_deleted_cause_used = InvitationFactory(
        family=data_test.family,
        expired_at=timezone.now() - timezone.timedelta(days=1),
        is_used=True,
    )
    should_not_be_deleted_cause_not_family = InvitationFactory(
        expired_at=timezone.now() + timezone.timedelta(days=1)
    )

    # We need to send the auth_token in the headers
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.delete("/api/invitation/clean_invitations/", headers=headers)

    assert response.status_code == 200

    # We check that the code is in the database
    invitations = Invitation.objects.all()

    assert len(invitations) == 3
    assert should_not_be_deleted_cause_active in invitations
    assert should_not_be_deleted_cause_used in invitations
    assert should_not_be_deleted_cause_not_family in invitations
    assert should_be_deleted_cause_perimed not in invitations


@pytest.mark.django_db
def test_create_invitation_with_max_invitations(client, data_test):
    """Test the deletion of expired and unused invitations."""

    # Given a family with 1 member and 1 invitation active with FREE plan (max_members = 2)
    InvitationFactory(
        family=data_test.family,
        is_used=False,
        expired_at=timezone.now() + timezone.timedelta(days=1),
    )

    # When I try to create a new invitation
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.get("/api/invitation/", headers=headers)

    # Then I should get a 403 error cause he can use the still active invitation
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_invitation_but_now_with_basic_plan(client, data_test):
    """Test the deletion of expired and unused invitations."""

    # Given a family with 1 member and 1 invitation active with BASIC plan (max_members = 3)
    settings = FamilySettings.objects.filter(family=data_test.family).first()
    settings.subscription_plan = "BASIC"
    settings.save()

    InvitationFactory(
        family=data_test.family,
        is_used=False,
        expired_at=timezone.now() + timezone.timedelta(days=1),
    )

    # When I try to create a new invitation
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}
    response = client.get("/api/invitation/", headers=headers)

    # Then I should get a 201 response, because he can have a 3rd member
    assert response.status_code == 201
