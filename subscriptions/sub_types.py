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


class PlanInformations(TypedDict):
    max_members: int
    max_possible_tasks: int
    max_ephemeral_tasks: int
    amount_cent: int
    reduction: float


SUBSCRIPTION_PLANS_RESTRICTIONS: dict[SubscriptionPlanChoices, PlanInformations] = {
    "FREE": {
        "max_members": 2,
        "max_possible_tasks": 5,
        "max_ephemeral_tasks": 3,
        "amount_cent": 0,
        "reduction": 0,
    },
    "BASIC": {
        "max_members": 3,
        "max_possible_tasks": 10,
        "max_ephemeral_tasks": 10,
        "amount_cent": 390,
        "reduction": 0.5,
    },
    "PREMIUM": {
        "max_members": 5,
        "max_possible_tasks": 15,
        "max_ephemeral_tasks": 100,
        "amount_cent": 990,
        "reduction": 0.6,
    },
}

CHANGE_PLAN_SURCHARGE = 100
