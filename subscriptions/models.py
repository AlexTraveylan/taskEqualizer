import uuid

from django.db import models

from subscriptions.sub_types import PaymentStatusChoices, SubscriptionPlanChoices
from tasks_api.family.models import Family


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
    )
    subscription_plan = models.CharField(
        max_length=10,
        choices=SubscriptionPlanChoices.choices,
        default=SubscriptionPlanChoices.FREE,
    )
    member_id = models.CharField(max_length=255)
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="subscriptions"
    )
