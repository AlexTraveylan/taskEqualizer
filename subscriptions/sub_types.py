from typing import TypedDict

from django.db import models


class PaymentStatusChoices(models.TextChoices):
    """Payment choices."""

    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"
    FAILED = "FAILED", "Failed"


class SubscriptionPlanChoices(models.TextChoices):
    """Choices for the subscription plan field."""

    FREE = "FREE", "Free"
    BASIC = "BASIC", "Basic"
    PREMIUM = "PREMIUM", "Premium"


class Restritions(TypedDict):
    max_members: int
    max_possible_tasks: int
    max_ephemeral_tasks: int


SUBSCRIPTION_PLANS_RESTRICTIONS: dict[SubscriptionPlanChoices, Restritions] = {
    "FREE": {
        "max_members": 2,
        "max_possible_tasks": 5,
        "max_ephemeral_tasks": 3,
    },
    "BASIC": {
        "max_members": 5,
        "max_possible_tasks": 20,
        "max_ephemeral_tasks": 15,
    },
    "PREMIUM": {
        "max_members": 10,
        "max_possible_tasks": 50,
        "max_ephemeral_tasks": 40,
    },
}
