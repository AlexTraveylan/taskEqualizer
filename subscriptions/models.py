from django.db import models

from subscriptions.sub_types import PaymentStatusChoices


class Subscription(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=10,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
    )
