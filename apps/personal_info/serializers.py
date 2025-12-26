# apps/personal_Info/serializers.py
from rest_framework import serializers
from .models import personal_info

class PersonalInfoSerializer(serializers.ModelSerializer):
    # optional: show username of the user
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = personal_info
        fields = ['id', 'name', 'description', 'image',  'user']
