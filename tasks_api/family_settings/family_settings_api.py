from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from auth_api.auth_token import CustomRequest, login_token_required
from tasks_api.family_settings.models import FamilySettings
from tasks_api.family_settings.schemas import FamilySettingsLocaleSchemaIn

router = Router()


@router.get("/", tags=["settings"])
@login_token_required
def get_settings(request: CustomRequest):
    settings = get_object_or_404(FamilySettings, family=request.member.family)

    return JsonResponse(settings.to_dict(), status=200)


@router.put("/", tags=["settings"])
@login_token_required
def update_locale(request: CustomRequest, payload: FamilySettingsLocaleSchemaIn):
    settings = get_object_or_404(FamilySettings, family=request.member.family)
    settings.locale = payload.locale
    settings.save()

    return JsonResponse(settings.to_dict(), status=200)
