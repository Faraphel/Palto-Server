"""
Views for the Palto project.

A view is what control the content of a page, prepare the correct data, react to a form, render the correct template.
"""
import uuid
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from Palto.Palto import models
from Palto.Palto.forms import LoginForm
from Palto.Palto.utils import get_object_or_none

ELEMENT_PER_PAGE: int = 30


# Create your views here.
def homepage_view(request: WSGIRequest):
    return render(request, "Palto/homepage.html")


def login_view(request: WSGIRequest):
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
def logout_view(request: WSGIRequest):
    # disconnect the user from the website
    logout(request)
    # redirect him to the main page
    return redirect("Palto:homepage")


@login_required
def profile_view(request: WSGIRequest, profile_id: uuid.UUID = None):
    if profile_id is None:
        # if the profile id is not given, redirect to the page of the current user.
        return redirect("Palto:profile", request.user.id)

    # get the corresponding user from its id.
    profile = get_object_or_404(models.User, id=profile_id)

    # prepare the data and the "complex" query for the template
    profile_departments_data = {
        department: {
            "is_manager": profile in department.managers.all(),
            "managing_units": models.TeachingUnit.objects.filter(department=department, managers=profile).all(),
            "teaching_units": models.TeachingUnit.objects.filter(department=department, teachers=profile).all(),
            "student_groups": models.StudentGroup.objects.filter(department=department, students=profile).all(),
        }

        for department in profile.related_departments
    }

    # render the page
    return render(
        request,
        "Palto/profile.html",
        context=dict(
            profile=profile,
            profile_departments_data=profile_departments_data,
        )
    )


@login_required
def teaching_session_list_view(request: WSGIRequest):
    # get all the sessions that the user can see, sorted by starting date
    raw_sessions = models.TeachingSession.all_visible_by_user(request.user).order_by("start")
    # paginate them to avoid having too many elements at the same time
    paginator = Paginator(raw_sessions, ELEMENT_PER_PAGE)

    # get only the session for the requested page
    page = request.GET.get("page", 0)
    sessions = paginator.get_page(page)

    # render the page
    return render(
        request,
        "Palto/teaching_session_list.html",
        context=dict(
            sessions=sessions
        )
    )


@login_required
def teaching_session_view(request: WSGIRequest, session_id: uuid.UUID):
    session = get_object_or_404(models.TeachingSession, id=session_id)

    if session not in models.TeachingSession.all_visible_by_user(request.user):
        # TODO: syntaxic sugar session.visible_by_user(request.user)
        return HttpResponseForbidden()

    # prepare the data and the "complex" query for the template
    session_students_data = {
        student: {
            "attendance": get_object_or_none(
                models.Attendance.objects,
                session=session,
                student=student
            ),
            "absence": get_object_or_none(
                models.Absence.objects,
                student=student,
                start__gte=session.start, end__lte=session.end
            ),
        }

        for student in session.group.students.all()
    }

    # render the page
    return render(
        request,
        "Palto/teaching_session.html",
        context=dict(
            session=session,
            session_students_data=session_students_data,
        )
    )
