import base64
import secrets

from cryptography.fernet import Fernet

from TaskEqualizer.settings import AES_KEY


def generate_confirmation_token() -> str:
    return secrets.token_urlsafe(nbytes=32)


def encrypt(string_to_encrypt: str, key: bytes = AES_KEY) -> str:
    f = Fernet(key)
    encrypted = f.encrypt(string_to_encrypt.encode())

    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt(string_to_decrypt: str, key: bytes = AES_KEY) -> str:
    f = Fernet(key)
    decrypted = f.decrypt(base64.urlsafe_b64decode(string_to_decrypt))

    return decrypted.decode()
