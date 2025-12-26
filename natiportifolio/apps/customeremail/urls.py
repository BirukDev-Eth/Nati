from django.urls import path
from . import views

urlpatterns = [
    path("", views.ContactListCreate.as_view(), name="contacts-list-create"),
    path("<int:pk>/", views.ContactRetrieveUpdateDelete.as_view(), name="contacts-rud"),
]
