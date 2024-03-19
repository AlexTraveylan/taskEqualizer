"""
Module for the HeaderJwtToken class
"""

import datetime
import os
from functools import wraps

import jwt
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv

from tasks_api.member.models import Member

load_dotenv()

SECRET_KEY = str(os.getenv("SECRET_KEY"))


class HeaderJwtToken:
    """Class for the HeaderJwtToken object"""

    def __init__(self, user_id: str, expiration: datetime.datetime = None):
        self.user_id = user_id
        self.expiration = expiration or (
            datetime.datetime.now() + datetime.timedelta(days=1)
        )

    def to_dict(self):
        """Convert the object to a dict"""
        return {
            "user_id": str(self.user_id),
            "expiration": self.expiration.timestamp(),
        }

    def __repr__(self):
        return f"HeaderJwtToken(user_id={self.user_id}, expiration={self.expiration})"

    @classmethod
    def from_dict(cls, data: dict):
        """Create a HeaderJwtToken object from a dict"""

        expiration = data.get("expiration")
        user_id = data["user_id"]

        if expiration:
            expiration_date = datetime.datetime.fromtimestamp(expiration)
            return cls(user_id, expiration_date)

        return cls(user_id)

    def to_jwt_token(self) -> str:
        """Create a jwt token from the object"""
        return jwt.encode(
            self.to_dict(),
            key=SECRET_KEY,
            algorithm="HS256",
            headers={"alg": "HS256", "typ": "JWT"},
        )

    @classmethod
    def from_jwt_token(cls, token: str) -> "HeaderJwtToken":
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


# decorateur for endpoint that require a token


class CustomRequest(HttpRequest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member: Member | None = None
        self.auth_token: str | None = None


def login_token_required(func_):
    """Decorator to check if the user is logged in

    Put it before the route decorator like this:
        @router.get("/", tags=["family"])
        @login_token_required
        def retrieve_family(request: CustomRequest):

    Like this is not ok :
        @login_token_required
        @router.get("/", tags=["family"])
        def retrieve_family(request: CustomRequest):
    """

    @wraps(func_)
    def wrapper(*args, **kwargs):

        request = args[0]

        auth_token = request.COOKIES.get("auth_token")

        # check if the token is present
        if not auth_token:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        # decode the token
        decoded_token = HeaderJwtToken.from_jwt_token(auth_token)

        # check if the token is expired
        if decoded_token.is_expired():
            return JsonResponse({"message": "Unauthorized"}, status=401)

        # get the user from the token
        member = get_object_or_404(Member, id=decoded_token.user_id)
        request.member = member

        # refresh the token
        decoded_token.refresh()
        request.auth_token = decoded_token.to_jwt_token()

        return func_(*args, **kwargs)

    return wrapper
