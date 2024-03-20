import pytest

from auth_api.auth_token import HeaderJwtToken
from tasks_api.models import Family, Member


@pytest.mark.django_db
def test_list_members_by_family(client):
    family_for_test = Family.objects.create(family_name="Test Family")
    member_for_test = Member.objects.create(
        member_name="Test Member", family=family_for_test
    )

    token = HeaderJwtToken(member_for_test.id)
    headers = {"Cookie": f"auth_token={token.to_jwt_token()}"}

    response = client.get("/api/family/members/", headers=headers)

    assert response.status_code == 200

    body_response = response.json()

    assert len(body_response) == 1
    assert body_response[0]["id"] == str(member_for_test.id)
