from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListCreate.as_view(), name='projects-list-create'),
    path('<int:pk>/', views.ProjectRetrieveUpdateDelete.as_view(), name='projects-rud'),
]
