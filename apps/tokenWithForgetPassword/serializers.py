from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PasswordResetToken

User = get_user_model()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        email = email.strip().lower()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exist")
        return email


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        email = data["email"].strip().lower()
        token = data["token"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Invalid email"})

        try:
            reset_token = PasswordResetToken.objects.get(
                user=user,
                token=token,
                is_used=False
            )
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid or used token"})

        if not reset_token.is_valid():
            raise serializers.ValidationError({"token": "Token expired"})

        data["user"] = user
        data["reset_token"] = reset_token
        return data
