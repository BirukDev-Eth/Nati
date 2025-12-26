from django.urls import path
from .views import SendContactReply

urlpatterns = [
    path("send/", SendContactReply.as_view(), name="send-contact-reply"),
]
