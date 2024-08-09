import pytest
from cryptography.fernet import Fernet

from emailmanager.crypto import decrypt, encrypt


@pytest.fixture
def key():
    return Fernet.generate_key()


def test_encryt_and_decrypt_email(key):
    email = "alextraveylan@gmail.com"

    encrypted_email = encrypt(email, key)

    assert email == decrypt(encrypted_email, key)
