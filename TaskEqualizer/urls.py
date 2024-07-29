"""
URL configuration for TaskEqualizer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from auth_api.views import (
    login,
    register_create_family,
    register_with_invitation,
)
from subscriptions.views import create_checkout_session, stripe_webhook
from tasks_api.views import api as tasks_api

urlpatterns = [
    path("api/", tasks_api.urls),
    path("admin/", admin.site.urls),
    path("login", login, name="login"),
    path("register_create", register_create_family, name="register_create"),
    path("register_invite", register_with_invitation, name="register_invite"),
    path("checkout_session", create_checkout_session, name="checkout_session"),
    path("stripe_webhook", stripe_webhook, name="stripe_webhook"),
]
