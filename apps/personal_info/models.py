# apps/experience/models.py
from django.db import models
from django.conf import settings

class personal_info(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='personal_infos'
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    class Meta:
        db_table = "personal_info"   # ✅ exact table name

    def __str__(self):
        return self.name
