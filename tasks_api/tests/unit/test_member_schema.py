import pytest

from emailmanager.crypto import decrypt
from tasks_api.member.schemas import MemberSchemaIn


def test_member_schema_without_email():
    member = MemberSchemaIn(member_name="John")

    assert member.member_name == "John"
    assert member.email is None


@pytest.mark.parametrize(
    "valid_email",
    ["test@gmail.com", "test@gmail.fr", "test@test.com", "test@test.fr"],
)
def test_member_schema_with_valid_email(valid_email):
    member = MemberSchemaIn(member_name="John", email=valid_email)

    assert member.member_name == "John"
    assert decrypt(member.email) == valid_email


@pytest.mark.parametrize(
    "invalid_email",
    ["test@gmail", "test@gmail.com.fr", "test@.com", "test@.fr"],
)
def test_member_schema_with_invalid_email(invalid_email):
    with pytest.raises(ValueError):
        MemberSchemaIn(member_name="John", email=invalid_email)
