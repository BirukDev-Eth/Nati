from django.urls import path
from .views import PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path("request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
