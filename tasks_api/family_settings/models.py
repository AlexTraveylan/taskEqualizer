import uuid

from django.db import models

from subscriptions.sub_types import SubscriptionPlanChoices


class LocaleChoices(models.TextChoices):
    """Choices for the locale field."""

    FR = "fr", "French"
    EN = "en", "English"
    DE = "de", "German"


class FamilySettings(models.Model):
    """Model for the family settings table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription_plan = models.CharField(
        max_length=10,
        choices=SubscriptionPlanChoices.choices,
        default=SubscriptionPlanChoices.FREE,
    )
    locale = models.CharField(
        max_length=10,
        choices=LocaleChoices.choices,
        default=LocaleChoices.EN,
    )
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="family_settings"
    )

    def __str__(self):
        return str(self.subscription_plan)

    def __repr__(self) -> str:
        return f"FamilySettings(id={self.id}, subscription_plan={self.subscription_plan}, locale={self.locale}, family={self.family.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "subscription_plan": self.subscription_plan,
            "locale": self.locale,
            "family": self.family.id,
        }

    class Meta:
        """Meta class for the Family settings model."""

        db_table = "family_settings"
