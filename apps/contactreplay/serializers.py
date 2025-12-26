from rest_framework import serializers
from .models import ContactReply

class ContactReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactReply
        fields = ["id", "contact", "reply_text"]
