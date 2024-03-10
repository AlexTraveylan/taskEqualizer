import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from auth_api.auth_token import HeaderJwtToken, login_token_required


@csrf_exempt
def login(request):
    if not request.method == "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        response = JsonResponse({"message": "Login successful"}, status=200)
        token = HeaderJwtToken(username=username)
        response.set_cookie("auth_token", token.to_jwt_token())
        return response
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=401)


@csrf_exempt
def register(request):
    """Register a new user."""

    if not request.method == "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse(
            {"message": "Username and password are required"}, status=400
        )

    user = User.objects.filter(username=username).first()
    if user:
        return JsonResponse({"message": "Username already exists"}, status=400)

    User.objects.create_user(username=username, password=password)
    token = HeaderJwtToken(username=username)
    response = JsonResponse({"message": "User created"}, status=201)
    response.set_cookie("auth_token", token.to_jwt_token())

    return response


@login_token_required
def get_user(request):
    return JsonResponse({"username": request.user.username})
