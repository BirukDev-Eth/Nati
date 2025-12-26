# apps/resume/serializers.py
from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    # optional: show username of the user
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Resume
        fields = [ 'url', 'user']