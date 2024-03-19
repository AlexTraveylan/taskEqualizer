import datetime
import json
import time
import uuid

from django.http import Http404, JsonResponse
from django.test import TestCase

from auth_api.auth_token import CustomRequest, HeaderJwtToken, login_token_required
from tasks_api.family.models import Family
from tasks_api.member.models import Member


class HeaderJwtTokenTestCase(TestCase):
    def setUp(self):
        self.user_id = "123"
        self.token = HeaderJwtToken(self.user_id)

    def test_to_dict(self):
        expected_dict = {
            "user_id": self.user_id,
            "expiration": self.token.expiration.timestamp(),
        }
        self.assertEqual(self.token.to_dict(), expected_dict)

    def test_from_dict(self):
        data = {
            "user_id": self.user_id,
            "expiration": self.token.expiration.timestamp(),
        }
        token = HeaderJwtToken.from_dict(data)
        self.assertEqual(token.user_id, self.user_id)

    def test_to_jwt_token(self):
        jwt_token = self.token.to_jwt_token()
        self.assertIsInstance(jwt_token, str)

    def test_from_jwt_token(self):
        jwt_token = self.token.to_jwt_token()
        token = HeaderJwtToken.from_jwt_token(jwt_token)
        self.assertEqual(token.user_id, self.user_id)

    def test_refresh(self):
        old_expiration = self.token.expiration
        time.sleep(0.01)
        self.token.refresh()
        self.assertGreater(self.token.expiration, old_expiration)

    def test_is_expired(self):
        self.assertFalse(self.token.is_expired())
        self.token.expiration = datetime.datetime.now() - datetime.timedelta(days=1)
        self.assertTrue(self.token.is_expired())


class LoginTokenRequiredTestCase(TestCase):
    def setUp(self):
        self.request = CustomRequest()

    def test_login_token_required_with_valid_token(self):
        user_id = uuid.uuid4()
        valid_token = HeaderJwtToken(user_id)
        family = Family.objects.create(family_name="test")
        Member.objects.create(id=user_id, member_name="test", family=family)
        self.request.COOKIES = {"auth_token": valid_token.to_jwt_token()}

        @login_token_required
        def dummy_view(request):
            return JsonResponse({"message": "Success"})

        response = dummy_view(self.request)
        self.assertEqual(response.status_code, 200)

        response_content = response.content.decode("utf-8")
        response_dict = json.loads(response_content)

        self.assertEqual(response_dict, {"message": "Success"})

    def test_login_token_required_with_missing_token(self):
        self.request.COOKIES = {}

        @login_token_required
        def dummy_view(request):
            return JsonResponse({"message": "Success"})

        response = dummy_view(self.request)
        self.assertEqual(response.status_code, 401)

        response_content = response.content.decode("utf-8")
        response_dict = json.loads(response_content)

        self.assertEqual(response_dict, {"message": "Unauthorized"})

    # def test_login_token_required_with_expired_token(self):

    #     expired_token = HeaderJwtToken("test")
    #     expired_token.expiration = datetime.datetime.now() - datetime.timedelta(days=1)
    #     self.request.COOKIES = {"auth_token": expired_token.to_jwt_token()}

    #     @login_token_required
    #     def dummy_view(request):
    #         return JsonResponse({"message": "Success"})

    #     response = dummy_view(self.request)
    #     self.assertEqual(response.status_code, 401)

    #     response_content = response.content.decode("utf-8")
    #     response_dict = json.loads(response_content)

    #     self.assertEqual(response_dict, {"message": "Unauthorized"})

    def test_login_token_required_with_invalid_user(self):

        user_id = uuid.uuid4()
        invalid_token = HeaderJwtToken(user_id)
        self.request.COOKIES = {"auth_token": invalid_token.to_jwt_token()}

        @login_token_required
        def dummy_view(request):
            return JsonResponse({"message": "Success"})

        with self.assertRaises(Http404):
            dummy_view(self.request)
