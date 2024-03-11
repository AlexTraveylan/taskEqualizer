from django.shortcuts import get_object_or_404
from ninja import Router

from tasks_api.models import Family
from tasks_api.schema import (
    FamilySchemaIn,
    FamilySchemaOut,
    MemberSchemaOut,
    PossibleTaskSchemaOut,
)

router = Router()


@router.post("/", response=FamilySchemaOut, tags=["family"])
def create_family(request, payload: FamilySchemaIn):
    """Create a family."""

    new_family = Family.objects.create(**payload.dict())

    return new_family


@router.get("/", response=list[FamilySchemaOut], tags=["family"])
def list_families(request):
    """List all families."""
    families = Family.objects.all()

    return families


@router.get("/{family_id}/members/", response=list[MemberSchemaOut], tags=["family"])
def list_members_by_family(request, family_id: int):
    """List all members by family."""

    family = get_object_or_404(Family, id=family_id)

    members = family.members.all()

    return members


@router.get(
    "/{family_id}/possibles_tasks/",
    response=list[PossibleTaskSchemaOut],
    tags=["family"],
)
def list_possibles_tasks_by_family(request, family_id: int):
    """List all possible tasks by family."""

    family = get_object_or_404(Family, id=family_id)

    possible_tasks = family.possible_tasks.all()

    return possible_tasks


@router.get("/{family_id}", response=FamilySchemaOut, tags=["family"])
def retrieve_family(request, family_id: int):
    """Retrieve a family."""

    family = get_object_or_404(Family, id=family_id)

    return family


@router.put("/{family_id}", response=FamilySchemaOut, tags=["family"])
def update_family(request, family_id: int, payload: FamilySchemaIn):
    """Update a family."""

    family = get_object_or_404(Family, id=family_id)

    for key, value in payload.dict().items():
        setattr(family, key, value)

    family.save()

    return family


@router.delete("/{family_id}", tags=["family"])
def delete_family(request, family_id: int):
    """Delete a family."""

    family = get_object_or_404(Family, id=family_id)

    family.delete()

    return {"message": "Family deleted successfully."}
