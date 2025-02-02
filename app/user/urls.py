"""
Define URL patterns.
"""

from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create-user"),
    path("token/", views.CreateTokenView.as_view(), name="find-token"),
]
