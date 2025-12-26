from django.urls import path
from .views import EducationListCreate, EducationRetrieveUpdateDelete

urlpatterns = [
    path('', EducationListCreate.as_view(), name='education-list-create'),
    path('<int:pk>/', EducationRetrieveUpdateDelete.as_view(), name='education-detail'),
]
