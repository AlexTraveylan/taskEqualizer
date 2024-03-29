import json
import time
import uuid
from datetime import datetime, timedelta

import pytest
from django.http import Http404, JsonResponse

from auth_api.auth_token import CustomRequest, HeaderJwtToken, login_token_required
from tasks_api.family.models import Family
from tasks_api.member.models import Member


@pytest.fixture
def token():
    user_id = "123"
    return HeaderJwtToken(user_id)


def test_to_dict(token):
    expected_dict = {
        "user_id": token.user_id,
        "expiration": token.expiration.timestamp(),
    }
    assert token.to_dict() == expected_dict


def test_from_dict(token):
    data = {
        "user_id": token.user_id,
        "expiration": token.expiration.timestamp(),
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
    token.expiration = datetime.now() - timedelta(days=1)
    assert token.is_expired()


@pytest.fixture
def custom_request():
    return CustomRequest()


@pytest.mark.django_db
def test_login_token_required_with_valid_token(custom_request):
    user_id = uuid.uuid4()
    valid_token = HeaderJwtToken(user_id)
    family = Family.objects.create(family_name="test")
    Member.objects.create(id=user_id, member_name="test", family=family)
    custom_request.COOKIES = {"auth_token": valid_token.to_jwt_token()}

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
    expired_token = HeaderJwtToken("test")
    expired_token.expiration = datetime.now() - timedelta(hours=1)
    custom_request.COOKIES = {"auth_token": expired_token.to_jwt_token()}

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
    custom_request.COOKIES = {"auth_token": invalid_token.to_jwt_token()}

    @login_token_required
    def dummy_view(request):
        return JsonResponse({"message": "Success"})

    with pytest.raises(Http404):
        dummy_view(custom_request)
