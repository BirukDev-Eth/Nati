from django.db import models
from apps.customeremail.models import ContactMessage

class ContactReply(models.Model):
    contact = models.ForeignKey(
        ContactMessage,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    reply_text = models.TextField()
    sent_to = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.sent_to}"
