from allauth.account.utils import send_email_confirmation
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse

from users.forms import EmailForm, ProfileForm, UsernameForm


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except AttributeError:
            return redirect_to_login(request.get_full_path())

    return render(request, "users/profile.html", {"profile": profile})


@login_required
def edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")

    if request.path == reverse("profile-onboarding"):
        onboarding = True
    else:
        onboarding = False

    return render(
        request, "users/profile_edit.html", {"form": form, "onboarding": onboarding}
    )


@login_required
def settings_view(request):
    return render(request, "users/profile_settings.html")


@login_required
def email_change(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, "partials/email_form.html", {"form": form})

    if request.method == "POST":
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f"{email} is already in use.")
                return redirect("profile-settings")

            form.save()

            # Then Signal updates emailaddress and set verified to False

            # Then send confirmation email
            send_email_confirmation(request, request.user)

            return redirect("profile-settings")
        else:
            messages.warning(request, "Email not valid or already in use")
            return redirect("profile-settings")

    return redirect("profile-settings")


@login_required
def username_change(request):
    if request.htmx:
        form = UsernameForm(instance=request.user)
        return render(request, "partials/username_form.html", {"form": form})

    if request.method == "POST":
        form = UsernameForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Username updated successfully.")
            return redirect("profile-settings")
        else:
            messages.warning(request, "Username not valid or already in use")
            return redirect("profile-settings")

    return redirect("profile-settings")


@login_required
def email_verify(request):
    send_email_confirmation(request, request.user)
    return redirect("profile-settings")


@login_required
def delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Account deleted, what a pity")
        return redirect("home")

    return render(request, "users/profile_delete.html")
