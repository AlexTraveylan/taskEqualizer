from django.db import models

from emailmanager.crypto import decrypt
from tasks_api.member.models import Member


class EmailConfirmationToken(models.Model):
    encrypted_email = models.EmailField(max_length=254, unique=True)
    token = models.CharField(max_length=255, unique=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="email_confirmation_token"
    )

    def __str__(self):
        return f"Confirmation token for {self.email}"

    def __repr__(self):
        return f"ConfirmationToken(id={self.id}, encrypted_email={self.encrypted_email}, token={self.token}, is_confirmed={self.is_confirmed}, created_at={self.created_at}, member={self.member.id})"

    class Meta:
        db_table = "email_confirmation_token"

    def get_email(self):
        return decrypt(self.encrypted_email)
