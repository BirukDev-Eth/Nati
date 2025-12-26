# apps/experience/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResumeListCreate.as_view(), name='resume-list-create'),
    path('<int:pk>/', views.ResumeRetrieveUpdateDelete.as_view(), name='resume-rud'),
]
