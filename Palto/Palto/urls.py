"""
Urls for the Palto project's API.

This file list all the urls for the Palto API.
"""

from django.urls import path
from Palto.Palto import views

app_name = "Palto"

urlpatterns = [
    # Base
    path("", views.homepage_view, name="homepage"),

    # User
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="my_profile"),
    path("profile/<uuid:profile_id>/", views.profile_view, name="profile"),
    path("teaching_sessions/", views.teaching_session_list_view, name="teaching_session_list"),
    path("teaching_sessions/<uuid:session_id>/", views.teaching_session_view, name="teaching_session"),
]
