"""All public routes for one language namespace."""
from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("therapy/", views.therapy, name="therapy"),
    path("contacts/", views.contacts, name="contacts"),
]
