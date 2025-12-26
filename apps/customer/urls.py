# apps/experience/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerListCreate.as_view(), name='customer-list-create'),
    path('<int:pk>/', views.CustomerRetrieveUpdateDelete.as_view(), name='customer-rud'),
]
