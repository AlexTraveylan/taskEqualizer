from ninja import Schema
from ninja.orm import create_schema

from tasks_api.family_settings.models import FamilySettings, LocaleChoices


class FamilySettingsLocaleSchemaIn(Schema):
    locale: LocaleChoices


MemberSchemaOut = create_schema(FamilySettings)
