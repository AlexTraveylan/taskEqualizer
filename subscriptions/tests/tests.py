import pytest


@pytest.mark.django_db
def test_get_plans_informations(client):
    response = client.get(
        "/plans_informations",
        content_type="application/json",
    )

    assert response.status_code == 200

    data = response.json()

    assert "FREE" in data
    assert "BASIC" in data
    assert "PREMIUM" in data
