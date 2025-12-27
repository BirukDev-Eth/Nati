from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.customeremail.models import ContactMessage
from .models import ContactReply
from .serializers import ContactReplySerializer
from apps.contactreplay.utils import send_email  # ✅ Resend email helper


class SendContactReply(APIView):
    def post(self, request):
        serializer = ContactReplySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        contact = serializer.validated_data["contact"]
        reply_text = serializer.validated_data["reply_text"]

        # ✅ Send email via Resend (API-based, non-SMTP)
        send_email(
            subject=f"Re: {contact.subject}",
            content=reply_text,
            to_email=contact.email,
        )

        # ✅ Save reply
        ContactReply.objects.create(
            contact=contact,
            reply_text=reply_text,
            sent_to=contact.email,
        )

        # ✅ Mark original message as read
        contact.is_read = True
        contact.save(update_fields=["is_read"])

        return Response(
            {"message": "Reply sent successfully"},
            status=status.HTTP_200_OK,
        )
