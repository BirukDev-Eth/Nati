from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class PasswordResetToken(models.Model):
    """
    Stores password reset tokens linked to a user
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens"
    )
    token = models.CharField(max_length=255, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.email} - {self.token}"

    @classmethod
    def create_token(cls, user, minutes=15):
        """
        Create a reset token for an existing user
        """
        token = uuid.uuid4().hex
        return cls.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timezone.timedelta(minutes=minutes)
        )

    def is_valid(self):
        """
        Check if token is valid (not expired & not used)
        """
        return not self.is_used and timezone.now() <= self.expires_at
