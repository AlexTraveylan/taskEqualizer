import pytest

from emailmanager.schemas import ContactFormSchema


def test_message_length_valid():
    schema = ContactFormSchema(
        email="test@example.com", message="This is a valid message"
    )
    assert schema.message == "This is a valid message"


def test_message_length_too_short():
    with pytest.raises(ValueError, match="Message is too short"):
        ContactFormSchema(email="test@example.com", message="Short")


def test_email_format_valid():
    schema = ContactFormSchema(email="test@example.com", message="Valid message")
    assert schema.email == "test@example.com"


def test_email_format_invalid():
    with pytest.raises(ValueError, match="Invalid email format"):
        ContactFormSchema(email="invalid_email", message="Valid message")
