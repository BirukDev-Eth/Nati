# apps/personal_info/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PersonalInfoListCreate.as_view(), name='personal-info-list-create'),
    path('<int:pk>/', views.PersonalInfoRetrieveUpdateDelete.as_view(), name='personal-info-rud'),
]
