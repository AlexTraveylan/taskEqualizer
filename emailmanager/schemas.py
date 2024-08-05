import re

from pydantic import BaseModel, field_validator


class ContactFormSchema(BaseModel):
    email: str
    message: str

    @field_validator("message")
    def message_length(cls, value):
        value = value.strip()

        if len(value) < 10:
            raise ValueError("Message is too short")

        return value

    @field_validator("email")
    def email_format(cls, value):
        value = value.strip()

        if re.match(r"[^@]+@[^@]+\.[^@]+", value) is None:
            raise ValueError("Invalid email format")

        return value
