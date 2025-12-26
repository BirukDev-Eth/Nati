from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from apps.customeremail.models import ContactMessage
from .models import ContactReply
from .serializers import ContactReplySerializer


class SendContactReply(APIView):
    def post(self, request):
        serializer = ContactReplySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        contact = serializer.validated_data["contact"]
        reply_text = serializer.validated_data["reply_text"]

        # Send email
        send_mail(
            subject=f"Re: {contact.subject}",
            message=reply_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            fail_silently=False,
        )

        # Save reply
        ContactReply.objects.create(
            contact=contact,
            reply_text=reply_text,
            sent_to=contact.email,
        )

        # Mark message as read
        contact.is_read = True
        contact.save()

        return Response(
            {"message": "Reply sent successfully"},
            status=status.HTTP_200_OK,
        )
