# apps/experience/models.py
from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resume'
    )
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.role} at {self.url}"
