from rest_framework import viewsets
from .models import Testimony
from .serializers import TestimonySerializer

class TestimonyViewSet(viewsets.ModelViewSet):
    queryset = Testimony.objects.all().order_by('-id')
    serializer_class = TestimonySerializer
