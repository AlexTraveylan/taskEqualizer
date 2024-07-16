import pytest

from auth_api.schemas import validate_family_name, validate_password, validate_username
from auth_api.validators import validate_invitation_code


@pytest.mark.parametrize(
    "invalid_password",
    [
        "a",
        "azerty",
        "AZERTY",
        "azertyuioipoiopqidpoqsid",
        "AZERTYUIOPIPOIPOQSDPOQSID",
        "123456789",
        "123456789azerty",
        "aA1",
        "alkjhazdkljsASDKQSJFDKSLM",
        "1324564aadfsdsgsdgfs",
        "ALDFSJMGKLJS1654",
    ],
)
def test_validate_password_with_invalid_passwords(invalid_password):
    with pytest.raises(ValueError):
        validate_password(invalid_password)


@pytest.mark.parametrize(
    "valid_password", ["ValidPassword123*", 'ValidPassword123*"*', "ValidPassword1"]
)
def test_validate_password_with_valid_passwords(valid_password):
    assert validate_password(valid_password) == valid_password


@pytest.mark.parametrize(
    "valid_username",
    [
        "valid_username",
        "valid_username1",
        "valid_username_",
        "abc😀",
        "my name",
        "My Name",
    ],
)
def test_validate_username_with_valid_usernames(valid_username):
    assert validate_username(valid_username) == valid_username


@pytest.mark.parametrize(
    "invalid_username",
    ["a", "a" * 26, "     a      "],
)
def test_validate_username_with_invalid_usernames(invalid_username):
    with pytest.raises(ValueError):
        validate_username(invalid_username)


@pytest.mark.parametrize(
    "valid_family_name",
    ["valid_f_name", "valid_famil1", "Valid family Name", "AI", "a" * 25],
)
def test_validate_family_name_with_valid_family_name(valid_family_name):
    assert validate_family_name(valid_family_name) == valid_family_name


@pytest.mark.parametrize(
    "invalid_family_name",
    [
        "a",
        "a" * 26,
    ],
)
def test_validate_family_name_with_invalid_family_name(invalid_family_name):
    with pytest.raises(ValueError):
        validate_family_name(invalid_family_name)


@pytest.mark.parametrize("valid_invitation_code", ["VALIDCOD", "12345678", "A1B2C3D4"])
def test_validate_invitation_code_with_valid_invitation_code(valid_invitation_code):
    assert validate_invitation_code(valid_invitation_code) == valid_invitation_code


@pytest.mark.parametrize(
    "invalid_invitation_code",
    [
        "abcdefgh",
        "A1B2C3D",
        "A1B2C3D4E",
    ],
)
def test_validate_invitation_code_with_invalid_invitation_code(invalid_invitation_code):
    with pytest.raises(ValueError):
        validate_invitation_code(invalid_invitation_code)
