import json

import pytest

from tasks_api.member.models import Member
from tasks_api.tests.factories import MemberFactory


@pytest.mark.django_db
def test_who_i_am(client, data_test):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    response = client.get("/api/member/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert body_response["member_id"] == str(data_test.member.id)


@pytest.mark.django_db
def test_update_member(client, data_test):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    payload = {"member_name": "new member name"}

    response = client.put("/api/member/", headers=headers, data=json.dumps(payload))

    assert response.status_code == 200

    new_member = Member.objects.get(id=data_test.member.id)
    assert new_member.member_name == "new member name"


@pytest.mark.django_db
def test_delete_member(client, data_test):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    member_to_delete = MemberFactory(family=data_test.family)

    response = client.delete(f"/api/member/{member_to_delete.id}", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert body_response["message"] == "Member deleted successfully."

    member = Member.objects.filter(id=member_to_delete.id).first()

    assert member is None


@pytest.mark.django_db
def test_delete_member_fail_if_not_from_family(client, data_test):
    headers = {"Authorization": f"Bearer {data_test.token.to_jwt_token()}"}

    member_to_delete = MemberFactory()

    response = client.delete(f"/api/member/{member_to_delete.id}", headers=headers)

    assert response.status_code == 404

    body_response = response.json()

    assert body_response["message"] == "Member not found."

    member = Member.objects.filter(id=member_to_delete.id).first()

    assert member == member_to_delete
