from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactListCreate(generics.ListCreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


class ContactRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
