import json
import time
import uuid

import pytest
from django.http import Http404, JsonResponse
from django.utils import timezone

from auth_api.auth_token import CustomRequest, HeaderJwtToken, login_token_required
from tasks_api.tests.factories import (
    FamilyFactory,
    FamilySettingsFactory,
    MemberFactory,
)


@pytest.fixture
def token():
    user_id = "123"
    return HeaderJwtToken(user_id)


def test_to_dict(token):
    expected_dict = {
        "user_id": token.user_id,
        "expiration": str(token.expiration),
    }
    assert token.to_dict() == expected_dict


def test_from_dict(token):
    data = {
        "user_id": token.user_id,
        "expiration": str(token.expiration),
    }
    new_token = HeaderJwtToken.from_dict(data)
    assert new_token.user_id == token.user_id


def test_to_jwt_token(token):
    jwt_token = token.to_jwt_token()
    assert isinstance(jwt_token, str)


def test_from_jwt_token(token):
    jwt_token = token.to_jwt_token()
    new_token = HeaderJwtToken.from_jwt_token(jwt_token)
    assert new_token.user_id == token.user_id


def test_refresh(token):
    old_expiration = token.expiration
    time.sleep(0.01)
    token.refresh()
    assert token.expiration > old_expiration


def test_is_expired(token):
    assert not token.is_expired()
    token.expiration = timezone.now() - timezone.timedelta(days=1)
    assert token.is_expired()


@pytest.fixture
def custom_request():
    return CustomRequest()


@pytest.mark.django_db
def test_login_token_required_with_valid_token(custom_request):
    user_id = uuid.uuid4()
    valid_token = HeaderJwtToken(user_id)
    family = FamilyFactory()
    MemberFactory(id=user_id, family=family)
    FamilySettingsFactory(family=family)
    custom_request.META["HTTP_AUTHORIZATION"] = f"Bearer {valid_token.to_jwt_token()}"

    @login_token_required
    def dummy_view(request):
        return JsonResponse({"message": "Success"})

    response = dummy_view(custom_request)
    assert response.status_code == 200

    response_content = response.content.decode("utf-8")
    response_dict = json.loads(response_content)

    assert response_dict == {"message": "Success"}


@pytest.mark.django_db
def test_login_token_required_with_missing_token(custom_request):
    custom_request.COOKIES = {}

    @login_token_required
    def dummy_view(request):
        return JsonResponse({"message": "Success"})

    response = dummy_view(custom_request)
    assert response.status_code == 401

    response_content = response.content.decode("utf-8")
    response_dict = json.loads(response_content)

    assert response_dict == {"message": "Unauthorized"}


@pytest.mark.django_db
def test_login_token_required_with_expired_token(custom_request):
    member = MemberFactory()
    expired_token = HeaderJwtToken(member.id)
    expired_token.expiration = timezone.now() - timezone.timedelta(hours=1)
    custom_request.META["HTTP_AUTHORIZATION"] = f"Bearer {expired_token.to_jwt_token()}"

    @login_token_required
    def dummy_view(request):
        return JsonResponse({"message": "Success"})

    response = dummy_view(custom_request)
    assert response.status_code == 401

    response_content = response.content.decode("utf-8")
    response_dict = json.loads(response_content)

    assert response_dict == {"message": "Unauthorized"}


@pytest.mark.django_db
def test_login_token_required_with_invalid_user(custom_request):
    user_id = uuid.uuid4()
    invalid_token = HeaderJwtToken(user_id)
    custom_request.META["HTTP_AUTHORIZATION"] = f"Bearer {invalid_token.to_jwt_token()}"

    @login_token_required
    def dummy_view(request):
        return JsonResponse({"message": "Success"})

    with pytest.raises(Http404):
        dummy_view(custom_request)
