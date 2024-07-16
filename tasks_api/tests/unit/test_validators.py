import pytest

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
