# apps/customer/serializers.py
from rest_framework import serializers

from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    # optional: show username of the user
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'subject', 'message', 'user']
