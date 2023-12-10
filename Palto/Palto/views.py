"""
Views for the Palto project.

A view is what control the content of a page, prepare the correct data, react to a form, render the correct template.
"""
import uuid
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from Palto.Palto.forms import LoginForm
from Palto.Palto.models import User


# Create your views here.
def homepage_view(request: HttpRequest):
    # TODO: homepage
    return HttpResponse("Hello there.")


def login_view(request: HttpRequest):
    # create a login form
    form_login = LoginForm(request.POST)

    if form_login.is_valid():
        # try to authenticate this user with the credentials
        user = authenticate(
            username=form_login.cleaned_data["username"],
            password=form_login.cleaned_data["password"]
        )

        if user is not None:
            # if the user was authenticated, log the user in.
            login(request, user)
            # redirect him to the main page
            return redirect("Palto:homepage")

        else:
            # otherwise the credentials were invalid.
            form_login.add_error(field=None, error="Invalid credentials.")

    # return the page
    return render(
        request,
        "Palto/login.html",
        context=dict(
            form_login=form_login
        )
    )


@login_required
def logout_view(request: HttpRequest):
    # disconnect the user from the website
    logout(request)
    # redirect him to the main page
    return redirect("Palto:homepage")


@login_required
def profile_view(request: HttpRequest, profile_id: uuid.UUID = None):
    if profile_id is None:
        # if the profile id is not given, redirect to the page of the current user.
        return redirect("Palto:profile", request.user.id)

    # get the corresponding user from its id.
    profile = get_object_or_404(User, id=profile_id)

    # render the page
    return render(
        request,
        "Palto/profile.html",
        context=dict(
            profile=profile
        )
    )
