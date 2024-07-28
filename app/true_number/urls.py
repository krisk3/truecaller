"""
Define URL patterns.
"""

from django.urls import path
from true_number import views

app_name = "true_number"

urlpatterns = [
    path("spam/", views.SpamNumberView.as_view(), name="create-user"),
    path("search-name/", views.SearchNameView.as_view(), name="search-name"),
    path("search-contact/", views.ContactSearchView.as_view(), name="search-contact"),
]
