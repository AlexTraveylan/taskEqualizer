import re

from TaskEqualizer.settings import MAX_POSSIBLE_TASK_NAME, MIN_POSSIBLE_TASK_NAME


def validate_task_name(value: str) -> str:
    value = value.strip()

    if len(value) < MIN_POSSIBLE_TASK_NAME:
        raise ValueError(
            f"Task name must be at least {MIN_POSSIBLE_TASK_NAME} characters long"
        )
    if len(value) > MAX_POSSIBLE_TASK_NAME:
        raise ValueError(
            f"Task name must be at most {MAX_POSSIBLE_TASK_NAME} characters long"
        )

    return value


def validate_email(value: str) -> str:
    value = value.strip()

    if not value:
        raise ValueError("Email cannot be empty.")

    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_regex, value):
        raise ValueError("Invalid email format.")

    if len(value) > 254:
        raise ValueError("Email is too long. Maximum length is 254 characters.")

    domain = value.split("@")[1]
    if "." not in domain:
        raise ValueError("Invalid domain in email address.")

    if domain.count(".") > 1:
        raise ValueError("Invalid domain in email address.")

    return value.lower()
