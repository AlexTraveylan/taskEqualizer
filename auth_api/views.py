import json
from datetime import datetime, timezone

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from auth_api.auth_token import HeaderJwtToken
from auth_api.schemas import RegisterCreateSchema, RegisterInviteSchema
from tasks_api.family.models import Family
from tasks_api.invitation.models import Invitation
from tasks_api.member.models import Member


@csrf_exempt
def login(request: HttpRequest):
    if not request.method == "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        member = Member.objects.filter(member_name=user.username).first()
        response = JsonResponse({"message": "Login successful"}, status=200)
        token = HeaderJwtToken(user_id=member.id)
        response.set_cookie(
            "auth_token",
            token.to_jwt_token(),
            httponly=True,
            secure=True,
            samesite=None,
        )
        return response
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=401)


@csrf_exempt
def register_create_family(request: HttpRequest):
    """Register a new user."""

    if not request.method == "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    data_used = {
        "family_name": data.get("family_name"),
        "username": data.get("username"),
        "password": data.get("password"),
    }

    parsed_data: RegisterCreateSchema | None = None
    try:
        parsed_data = RegisterCreateSchema(**data_used)
    except ValidationError:
        return JsonResponse({"message": "Missing informations"}, status=400)

    user = User.objects.filter(username=parsed_data.username).first()
    if user:
        return JsonResponse({"message": "Username already exists"}, status=400)

    family = Family.objects.create(family_name=parsed_data.family_name)
    user = User.objects.create_user(
        username=parsed_data.username, password=parsed_data.password
    )
    member = Member.objects.create(member_name=user.username, family=family)
    token = HeaderJwtToken(user_id=member.id)
    response = JsonResponse({"message": "User created"}, status=201)
    response.set_cookie(
        "auth_token", token.to_jwt_token(), httponly=True, secure=True, samesite=None
    )

    return response


@csrf_exempt
def register_with_invitation(request: HttpRequest):
    """Register a new user with an invitation code."""

    if not request.method == "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    data_used = {
        "username": data.get("username"),
        "password": data.get("password"),
        "invitation_code": data.get("invitation_code"),
    }

    # Check if the data is correct
    parsed_data: RegisterInviteSchema | None = None
    try:
        parsed_data = RegisterInviteSchema(**data_used)
    except ValidationError:
        return JsonResponse({"message": "Missing informations"}, status=400)

    # Check if the username already exists
    user = User.objects.filter(username=parsed_data.username).first()
    if user:
        return JsonResponse({"message": "Username already exists"}, status=400)

    # Get the invitation
    invitation = Invitation.objects.filter(code=parsed_data.invitation_code).first()

    if not invitation:
        return JsonResponse({"message": "Invalid invitation code"}, status=400)

    if invitation.is_used:
        return JsonResponse({"message": "Invitation already used"}, status=400)

    if datetime.now(timezone.utc) > invitation.expired_at:
        return JsonResponse({"message": "Invitation expired"}, status=400)

    # Create the user
    family = invitation.family
    user = User.objects.create_user(
        username=parsed_data.username, password=parsed_data.password
    )
    member = Member.objects.create(member_name=user.username, family=family)

    # Mark the invitation as used
    invitation.is_used = True
    invitation.save()

    # Create the token
    token = HeaderJwtToken(user_id=member.id)
    response = JsonResponse({"message": "User created"}, status=201)
    response.set_cookie(
        "auth_token", token.to_jwt_token(), httponly=True, secure=True, samesite=None
    )

    return response


def logout(request: HttpRequest):
    response = JsonResponse({"message": "Logout successful"}, status=200)
    response.delete_cookie("auth_token")
    return response
