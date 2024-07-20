import pytest

from tasks_api.ephemeral_task.schemas import EphemeralTaskSchemaIn
from tasks_api.validators import validate_task_name


@pytest.mark.parametrize(
    "valid_p_task_name",
    [
        "TA",
        "Task",
        "Task name",
        "Task name 1",
        "Cuisine",
        "Vaisselle",
        "Ménage",
        "Ménage 2",
        "a" * 13,
    ],
)
def test_validate_task_name_with_valid_names(valid_p_task_name):
    assert validate_task_name(valid_p_task_name) == valid_p_task_name


@pytest.mark.parametrize(
    "invalid_p_task_name",
    [
        "T",
        "T" * 14,
    ],
)
def test_validate_task_name_with_invalid_names(invalid_p_task_name):
    with pytest.raises(ValueError):
        validate_task_name(invalid_p_task_name)


@pytest.mark.parametrize(
    ("ephemeral_task_name", "description", "value"),
    [
        ("Task", "Task description", 1),
        ("Task 1", "Task description 1", 2),
        ("Task 2", "Task description 2", 5),
        ("Task 3", "Task description 3", 10),
        ("Task 4", "Task description 4", 15),
        ("Task 5", "Task description 5", 30),
        ("Task 6", "Task description 6", 60),
        ("Task 7", "Task description 7", 120),
    ],
)
def test_validate_ephemeral_schema_with_valid_schema(
    ephemeral_task_name, description, value
):
    e_task = EphemeralTaskSchemaIn(
        ephemeral_task_name=ephemeral_task_name,
        description=description,
        value=value,
    )

    assert e_task.ephemeral_task_name == ephemeral_task_name


@pytest.mark.parametrize(
    ("ephemeral_task_name", "description", "value"),
    [
        # Invalid ephemeral task name too short
        ("T", "Task description", 1),
        # Invalid ephemeral task name too long
        ("T" * 26, "Task description 1", 2),
        # Invalid description too long
        ("Task 2", "D" * 1001, 5),
        # Invalid value
        ("Task 3", "Task description 3", 11),
        ("Task 4", "Task description 4", 16),
        ("Task 5", "Task description 5", 31),
        ("Task 6", "Task description 6", 61),
        ("Task 7", "Task description 7", 121),
    ],
)
def test_validate_ephemeral_schema_with_invalid_schema(
    ephemeral_task_name, description, value
):
    with pytest.raises(ValueError):
        EphemeralTaskSchemaIn(
            ephemeral_task_name=ephemeral_task_name,
            description=description,
            value=value,
        )
