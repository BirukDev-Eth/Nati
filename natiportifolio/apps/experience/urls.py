# apps/experience/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExperienceListCreate.as_view(), name='experience-list-create'),
    path('<int:pk>/', views.ExperienceRetrieveUpdateDelete.as_view(), name='experience-rud'),
]
