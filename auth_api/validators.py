import re

from TaskEqualizer.settings import (
    INVITATION_CODE_SIZE,
    MAX_LENGTH_FAMILY_NAME,
    MAX_LENGTH_USERNAME,
    MIN_LENGTH_FAMILY_NAME,
    MIN_LENGTH_USERNAME,
)


def validate_family_name(value: str) -> str:
    value = value.strip()

    if len(value) < MIN_LENGTH_FAMILY_NAME:
        raise ValueError(
            f"Family name must be at least {MIN_LENGTH_FAMILY_NAME} characters long"
        )

    if len(value) > MAX_LENGTH_FAMILY_NAME:
        raise ValueError(
            f"Family name must be at most {MAX_LENGTH_FAMILY_NAME} characters long"
        )

    return value


def validate_username(value: str) -> str:
    value = value.strip()

    if len(value) < MIN_LENGTH_USERNAME:
        raise ValueError(
            f"Username must be at least {MIN_LENGTH_USERNAME} characters long"
        )

    if len(value) > MAX_LENGTH_USERNAME:
        raise ValueError(
            f"Username must be at most {MAX_LENGTH_USERNAME} characters long"
        )

    if "@" in value:
        raise ValueError("Username cannot contain the @ symbol.")

    return value


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")

    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter")

    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter")

    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit")

    return value


def validate_invitation_code(value: str) -> str:
    value = value.strip()

    if len(value) != INVITATION_CODE_SIZE:
        raise ValueError(
            f"Invitation code must be {INVITATION_CODE_SIZE} characters long"
        )

    if not re.match("^[A-Z0-9]*$", value):
        raise ValueError(
            "Invitation code must contain only uppercase letters and digits"
        )

    return value
