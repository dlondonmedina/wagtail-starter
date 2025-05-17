from django.urls import path
from users.views import (
    profile_view,
    edit_view,
    settings_view,
    email_change,
    username_change,
    email_verify,
    delete_view,
)

urlpatterns = [
    path("", profile_view, name="profile"),
    path("profile-edit/", edit_view, name="profile-edit"),
    path("profile-onboarding/", edit_view, name="profile-onboarding"),
    path("profile-settings/", settings_view, name="profile-settings"),
    path("profile-email-change/", email_change, name="profile-email-change"),
    path("profile-username-change/", username_change, name="profile-username-change"),
    path("profile-email-verify/", email_verify, name="profile-email-verify"),
    path("profile-delete/", delete_view, name="profile-delete"),
]
