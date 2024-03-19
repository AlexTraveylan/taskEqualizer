import json
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase

from auth_api.views import login, logout, register_create_family
from tasks_api.family.models import Family
from tasks_api.member.models import Member

# Create your tests here.


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        family = Family.objects.create(family_name="testfamily")
        self.member = Member.objects.create(member_name="testuser", family=family)

    @patch("auth_api.views.authenticate")
    def test_login_success(self, mock_authenticate):
        mock_authenticate.return_value = self.user

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps({"username": "testuser", "password": "12345"})

        response = login(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("auth_token", response.cookies)

        content_str = response.content.decode("utf-8")
        json_data = json.loads(content_str)

        self.assertEqual(json_data["message"], "Login successful")

    @patch("auth_api.views.authenticate")
    def test_login_fail(self, mock_authenticate):
        mock_authenticate.return_value = None

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps(
            {"username": "testuser", "password": "wrong_password"}
        )

        response = login(request)

        self.assertEqual(response.status_code, 401)

        content_str = response.content.decode("utf-8")
        json_data = json.loads(content_str)

        self.assertEqual(json_data["message"], "Invalid credentials")


class RegisterCreateFamilyTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser")

    def test_register_succes(self):

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps(
            {
                "family_name": "testfamily",
                "username": "newuser",
                "password": "12345",
            }
        )

        response = register_create_family(request)

        self.assertEqual(response.status_code, 201)
        self.assertIn("auth_token", response.cookies)

        content_str = response.content.decode("utf-8")
        json_data = json.loads(content_str)

        self.assertEqual(json_data["message"], "User created")

    def test_register_fail_missing_informations(self):

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps(
            {
                "family_name": "testfamily",
                "username": "newuser",
            }
        )

        response = register_create_family(request)

        self.assertEqual(response.status_code, 400)

        content_str = response.content.decode("utf-8")
        json_data = json.loads(content_str)

        self.assertEqual(json_data["message"], "Missing informations")

    def test_register_fail_user_already_exist(self):

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps(
            {
                "family_name": "testfamily",
                "username": "testuser",
                "password": "12345",
            }
        )

        response = register_create_family(request)

        self.assertEqual(response.status_code, 400)

        content_str = response.content.decode("utf-8")
        json_data = json.loads(content_str)

        self.assertEqual(json_data["message"], "Username already exists")


class LogoutTest(TestCase):

    def test_logout(self):

        request = MagicMock()
        request.COOKIES = {"auth_token": "test_token"}

        response = logout(request)

        self.assertEqual(response.status_code, 200)

        self.assertNotIn("auth_token", response.cookies)

        json_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(json_data["message"], "Logout successful")
