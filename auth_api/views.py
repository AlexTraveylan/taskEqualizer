import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            response = JsonResponse({"message": "Login successful"})
            response.set_cookie("auth_token", "YOUR_AUTH_TOKEN_HERE")
            return response
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({"message": "User created"})
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
