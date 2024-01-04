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

from Palto.Palto import models, forms
from Palto.Palto.utils import get_object_or_none

ELEMENT_PER_PAGE: int = 30


# Create your views here.
def homepage_view(request: WSGIRequest):
    return render(request, "Palto/homepage.html")


def login_view(request: WSGIRequest):
    # create a login form

    if request.POST:
        form_login = forms.LoginForm(request.POST)

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
    else:
        form_login = forms.LoginForm()

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

    # check if the user is allowed to see this specific object
    if not profile.is_visible_by_user(request.user):
        return HttpResponseForbidden()

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
def teaching_unit_view(request: WSGIRequest, unit_id: uuid.UUID):
    unit = get_object_or_404(models.TeachingUnit, id=unit_id)

    # check if the user is allowed to see this specific object
    if not unit.is_visible_by_user(request.user):
        return HttpResponseForbidden()

    # render the page
    return render(
        request,
        "Palto/teaching_unit_view.html",
        context=dict(
            unit=unit,
        )
    )


@login_required
def teaching_session_view(request: WSGIRequest, session_id: uuid.UUID):
    session = get_object_or_404(models.TeachingSession, id=session_id)

    # check if the user is allowed to see this specific object
    if not session.is_visible_by_user(request.user):
        return HttpResponseForbidden()

    # prepare the data and the "complex" query for the template
    session_students_data = {
        student: {
            "attendance": get_object_or_none(models.Attendance.objects, session=session, student=student),
            "absence": get_object_or_none(session.related_absences, student=student)
        }

        for student in session.group.students.all()
    }

    # render the page
    return render(
        request,
        "Palto/teaching_session_view.html",
        context=dict(
            session=session,
            session_students_data=session_students_data,
        )
    )


@login_required
def absence_view(request: WSGIRequest, absence_id: uuid.UUID):
    absence = get_object_or_404(models.Absence, id=absence_id)

    # check if the user is allowed to see this specific object
    if not absence.is_visible_by_user(request.user):
        return HttpResponseForbidden()

    # render the page
    return render(
        request,
        "Palto/absence_view.html",
        context=dict(
            absence=absence,
        )
    )


@login_required
def new_absence_view(request: WSGIRequest):
    # check if the user can create an absence
    if not models.Absence.can_user_create(request.user):
        return HttpResponseForbidden()

    # create a form for the new absence
    form_new_absence = forms.NewAbsenceForm(request.user, request.POST, request.FILES)

    if form_new_absence.is_valid():
        print(form_new_absence.files, form_new_absence.cleaned_data)

        absence, is_created = models.Absence.objects.get_or_create(
            student=request.user,
            start=form_new_absence.cleaned_data["start"],
            end=form_new_absence.cleaned_data["end"],
            department=form_new_absence.cleaned_data["department"],
            message=form_new_absence.cleaned_data["message"],
        )

        if not is_created:
            # if the absence already existed, show an error
            form_new_absence.add_error(None, "This absence already exists.")

        else:
            # add the attachments files to the absence
            for file in form_new_absence.cleaned_data["attachments"]:
                absence.attachments.create(
                    content=file
                )

            return redirect("Palto:homepage")  # TODO(Faraphel): redirect to absence list

    # render the page
    return render(
        request,
        "Palto/absence_new.html",
        context=dict(
            form_new_absence=form_new_absence,
        )
    )


def absence_list_view(request):
    # get all the absences that the user can see, sorted by starting date
    raw_absences = models.Absence.all_visible_by_user(request.user).order_by("start")
    # paginate them to avoid having too many elements at the same time
    paginator = Paginator(raw_absences, ELEMENT_PER_PAGE)

    # get only the session for the requested page
    page = request.GET.get("page", 0)
    absences = paginator.get_page(page)

    # render the page
    return render(
        request,
        "Palto/absence_list.html",
        context=dict(
            absences=absences
        )
    )


@login_required
def department_view(request: WSGIRequest, department_id: uuid.UUID):
    department = get_object_or_404(models.Department, id=department_id)

    # check if the user is allowed to see this specific object
    if not department.is_visible_by_user(request.user):
        return HttpResponseForbidden()

    # render the page
    return render(
        request,
        "Palto/department_view.html",
        context=dict(
            department=department,
        )
    )


@login_required
def student_group_view(request: WSGIRequest, group_id: uuid.UUID):
    group = get_object_or_404(models.StudentGroup, id=group_id)

    # check if the user is allowed to see this specific object
    if not group.is_visible_by_user(request.user):
        return HttpResponseForbidden()

    # render the page
    return render(
        request,
        "Palto/student_group.html",
        context=dict(
            group=group,
        )
    )
