"""
Module for the HeaderJwtToken class
"""

from __future__ import annotations

from functools import wraps
from typing import TypedDict

import jwt
from dateutil import parser
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from TaskEqualizer.settings import SECRET_KEY, TOKEN_NAME
from tasks_api.member.models import Member


class TokenContent(TypedDict):
    user_id: str
    expiration: str


class HeaderJwtToken:
    """Class for the HeaderJwtToken object"""

    def __init__(self, user_id: str, expiration: timezone.datetime = None) -> None:
        self.user_id = str(user_id)
        self.expiration = expiration or (timezone.now() + timezone.timedelta(days=1))

    def to_dict(self) -> TokenContent:
        """Convert the object to a dict"""

        return TokenContent(user_id=self.user_id, expiration=str(self.expiration))

    def __repr__(self):
        return f"HeaderJwtToken(user_id={self.user_id}, expiration={self.expiration})"

    @classmethod
    def from_dict(cls, data: dict) -> HeaderJwtToken:
        """Create a HeaderJwtToken object from a dict"""

        expiration = data.get("expiration")
        user_id = data["user_id"]

        if expiration:
            expiration_date = parser.isoparse(expiration)
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
    def from_jwt_token(cls, token: str) -> HeaderJwtToken:
        """Create a HeaderJwtToken object from a jwt token"""
        data = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
        token = cls.from_dict(data)
        return token

    def refresh(self):
        """Refresh the token"""
        self.expiration = timezone.now() + timezone.timedelta(days=1)

    def is_expired(self):
        """Check if the token is expired"""
        return timezone.now() > self.expiration


# decorateur for endpoint that require a token


class CustomRequest(HttpRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member: Member = None
        self.auth_token: str = None


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

        auth_token = request.headers.get("Authorization")

        # check if the token is present
        if not auth_token:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        # Extract the token from the header
        auth_token = auth_token.split(" ")[1]

        # decode the token
        decoded_token = HeaderJwtToken.from_jwt_token(auth_token)

        # check if the token is expired
        if decoded_token.is_expired():
            response = JsonResponse({"message": "Unauthorized"}, status=401)
            response.delete_cookie(TOKEN_NAME)

            return response

        # get the user from the token
        member = get_object_or_404(Member, id=decoded_token.user_id)
        request.member = member

        # refresh the token
        decoded_token.refresh()
        request.auth_token = decoded_token.to_jwt_token()

        return func_(*args, **kwargs)

    return wrapper
