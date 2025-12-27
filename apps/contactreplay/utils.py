# utils/email.py
import resend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Set API key once
resend.api_key = settings.RESEND_API_KEY


def send_email(subject, content, to_email):
    try:
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": to_email,
            "subject": subject,
            "text": content,
        })
    except Exception as e:
        logger.error(f"Resend email failed: {e}")
        raise
