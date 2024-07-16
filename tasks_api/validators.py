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
