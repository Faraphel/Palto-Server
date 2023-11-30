"""
Admin for the Palto project.

The admin is the admin page configuration, describing which model should be visible and which field in the admin page.
"""

from django.contrib import admin

from .models import (Department, StudentGroup, TeachingUnit, StudentCard, TeachingSession, Attendance, Absence,
                     AbsenceAttachment, User)


# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("id", "username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff",)


@admin.register(Department)
class AdminDepartment(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("id", "name", "email")


@admin.register(StudentGroup)
class AdminStudentGroup(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "department")
    search_fields = ("id", "name", "owner", "department")


@admin.register(TeachingUnit)
class AdminTeachingUnit(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")


@admin.register(StudentCard)
class AdminStudentCard(admin.ModelAdmin):
    list_display = ("id", "uid", "owner")
    search_fields = ("id", "uid", "owner")
    readonly_fields = ("uid",)


@admin.register(TeachingSession)
class AdminTeachingSession(admin.ModelAdmin):
    list_display = ("id", "start", "end", "duration", "teacher")
    search_fields = ("id", "start", "end", "duration", "teacher")
    list_filter = ("start", "duration")


@admin.register(Attendance)
class AdminAttendance(admin.ModelAdmin):
    list_display = ("id", "date", "student")
    search_fields = ("id", "date", "student")
    list_filter = ("date",)


@admin.register(Absence)
class AdminAbsence(admin.ModelAdmin):
    list_display = ("id", "message", "student")
    search_fields = ("id", "message", "student")


@admin.register(AbsenceAttachment)
class AdminAbsenceAttachment(admin.ModelAdmin):
    list_display = ("id", "content", "absence")
    search_fields = ("id", "content", "absence")
