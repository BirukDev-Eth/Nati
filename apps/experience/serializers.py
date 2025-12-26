# apps/experience/serializers.py
from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    # optional: show username of the user
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'role', 'start_date', 'end_date', 'user']
