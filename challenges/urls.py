from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home),
    path("edit/", views.update_config_home, name="update_config_home"),
    path("challenge/new", views.create_or_edit_challenge, name="create_challenge"),
    path(
        "challenge/<int:challenge_id>/", views.challenge_detail, name="challenge_detail"
    ),
    path(
        "challenge/<int:challenge_id>/edit",
        views.create_or_edit_challenge,
        name="edit_challenge",
    ),
]
