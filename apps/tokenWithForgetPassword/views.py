from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import PasswordResetToken
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

import resend  # correct import for Resend Python SDK

User = get_user_model()

# Set the API key
resend.api_key = settings.RESEND_API_KEY


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip().lower()
        user = User.objects.get(email=email)

        reset_token = PasswordResetToken.create_token(user)

        # prepare email params
        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [email],
            "subject": "Password Reset Request",
            "html": (
                f"<p>Your password reset token is:</p>"
                f"<h2>{reset_token.token}</h2>"
                f"<p>This token will expire in 15 minutes.</p>"
            ),
        }

        # send email via Resend
        resend.Emails.send(params)

        return Response(
            {"message": "Password reset token sent to email"},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        reset_token.is_used = True
        reset_token.save()

        # prepare confirmation email
        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [user.email],
            "subject": "Password Changed Successfully",
            "html": "<p>Your password has been reset successfully.</p>",
        }

        resend.Emails.send(params)

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
        )
