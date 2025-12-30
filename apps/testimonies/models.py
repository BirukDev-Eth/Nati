from django.db import models

class Testimony(models.Model):  # <-- Name must match import
    id = models.AutoField(primary_key=True)
    message = models.TextField(default="")
    name = models.CharField(max_length=100, default="")
    position = models.CharField(max_length=100, default="")
    company = models.CharField(max_length=100, default="")
    image = models.URLField(default="https://randomuser.me/api/portraits/lego/1.jpg")

    def __str__(self):
        return f"{self.name} - {self.position}"
