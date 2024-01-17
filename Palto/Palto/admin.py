"""
Admin for the Palto project.

The admin is the admin page configuration, describing which model should be visible and which field in the admin page.
"""

from django.contrib import admin

from . import models


# TODO(Faraphel): plus de list_filter sur "department" ?


# Register your models here.
@admin.register(models.User)
class AdminUser(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("id", "username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff",)


@admin.register(models.Department)
class AdminDepartment(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("id", "name", "email")
    readonly_fields = ("id",)


@admin.register(models.StudentGroup)
class AdminStudentGroup(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "department")
    search_fields = ("id", "name", "owner", "department")
    list_filter = ("department",)
    readonly_fields = ("id",)


@admin.register(models.TeachingUnit)
class AdminTeachingUnit(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("id", "name", "email")
    readonly_fields = ("id",)


@admin.register(models.StudentCard)
class AdminStudentCard(admin.ModelAdmin):
    list_display = ("id", "uid", "department", "owner")
    search_fields = ("id", "uid", "department", "owner")
    readonly_fields = ("id", "uid",)
    list_filter = ("department",)


@admin.register(models.TeachingSession)
class AdminTeachingSession(admin.ModelAdmin):
    list_display = ("id", "start", "end", "unit", "duration", "teacher")
    search_fields = ("id", "start", "end", "unit", "duration", "teacher")
    readonly_fields = ("id",)
    list_filter = ("unit",)


@admin.register(models.Attendance)
class AdminAttendance(admin.ModelAdmin):
    list_display = ("id", "date", "student")
    search_fields = ("id", "date", "student")
    readonly_fields = ("id",)
    list_filter = ("date",)


@admin.register(models.Absence)
class AdminAbsence(admin.ModelAdmin):
    list_display = ("id", "message", "student", "start", "end")
    search_fields = ("id", "message", "student", "start", "end")
    readonly_fields = ("id",)
    list_filter = ("start", "end")


@admin.register(models.AbsenceAttachment)
class AdminAbsenceAttachment(admin.ModelAdmin):
    list_display = ("id", "content", "absence")
    search_fields = ("id", "content", "absence")
    readonly_fields = ("id",)
