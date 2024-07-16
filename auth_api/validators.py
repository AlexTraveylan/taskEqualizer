import re

from TaskEqualizer.settings import (
    MAX_LENGTH_FAMILY_NAME,
    MAX_LENGTH_USERNAME,
    MIN_LENGTH_FAMILY_NAME,
    MIN_LENGTH_USERNAME,
)


def validate_family_name(value: str) -> str:
    value = value.strip()

    if len(value) < MIN_LENGTH_FAMILY_NAME:
        raise ValueError("Family name must be at least 2 characters long")

    if len(value) > MAX_LENGTH_FAMILY_NAME:
        raise ValueError("Family name must be at most 25 characters long")

    return value


def validate_username(value: str) -> str:
    value = value.strip()

    if len(value) < MIN_LENGTH_USERNAME:
        raise ValueError("Username must be at least 2 characters long")

    if len(value) > MAX_LENGTH_USERNAME:
        raise ValueError("Username must be at most 25 characters long")

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
