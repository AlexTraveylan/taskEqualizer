"""
Module for the HeaderJwtToken class
"""

import datetime
import os

import jwt
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class HeaderJwtToken:
    """Class for the HeaderJwtToken object"""

    def __init__(self, username: str):
        self.username = username
        self.expiration = datetime.datetime.now() + datetime.timedelta(days=1)

    def to_dict(self):
        """Convert the object to a dict"""
        return {
            "username": self.username,
            "expiration": self.expiration.timestamp(),
        }

    def __repr__(self):
        return f"HeaderJwtToken(username={self.username}, expiration={self.expiration})"

    @classmethod
    def from_dict(cls, data: dict):
        """Create a HeaderJwtToken object from a dict"""
        return cls(username=data["username"])

    def to_jwt_token(self):
        """Create a jwt token from the object"""
        return jwt.encode(
            self.to_dict(),
            key=SECRET_KEY,
            algorithm="HS256",
            headers={"alg": "HS256", "typ": "JWT"},
        )

    @classmethod
    def from_jwt_token(cls, token: str):
        """Create a HeaderJwtToken object from a jwt token"""
        data = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
        token = cls.from_dict(data)
        return token

    def refresh(self):
        """Refresh the token"""
        self.expiration = datetime.datetime.now() + datetime.timedelta(days=1)

    def is_expired(self):
        """Check if the token is expired"""
        return datetime.datetime.now() > self.expiration


# decorateur pour les endpoints with django


def login_token_required(func_):
    """Decorator to check if the user is logged in"""

    def wrapper(*args, **kwargs):
        request = args[0]
        auth_token = request.COOKIES.get("auth_token")
        if not auth_token:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        decoded_token = HeaderJwtToken.from_jwt_token(auth_token)
        if decoded_token.is_expired():
            return JsonResponse({"message": "Unauthorized"}, status=401)

        user = get_object_or_404(User, username=decoded_token.username)
        request.user = user

        return func_(*args, **kwargs)

    return wrapper
