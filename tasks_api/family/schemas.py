from ninja.orm import create_schema

from TaskEqualizer.settings import STANDARD_EXCLUDE
from tasks_api.family.models import Family

FamilySchemaIn = create_schema(Family, exclude=STANDARD_EXCLUDE)
FamilySchemaOut = create_schema(Family)
