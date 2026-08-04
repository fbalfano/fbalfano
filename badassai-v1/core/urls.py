from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("members/", views.members, name="members"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("contact/", views.contact, name="contact"),
]
