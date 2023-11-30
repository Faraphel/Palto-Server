"""
Permissions for the Palto project's API v1.

A permission describe which user is allowed to see and modify which objet with the API
"""

from rest_framework import permissions

from Palto.Palto.models import (Department, TeachingUnit, StudentCard, StudentGroup, User, TeachingSession, Attendance,
                                Absence, AbsenceAttachment)


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the user is in one of the same department as the requesting user, allow read
            if obj in Department.multiple_related_users(request.user.related_departments):
                return True

        return False


class DepartmentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Department) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the group department is managed by the user, allow all
        if obj in request.user.managing_departments:
            return True

        if request.method in permissions.SAFE_METHODS:
            # allow read to everybody
            return True

        return False


class StudentGroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: StudentGroup) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the group department is managed by the user, allow all
        if obj.department in request.user.managing_departments:
            return True

        # if the user is the owner of the group, allow all
        if obj.owner is request.user:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the student is in the group, allow read
            if obj in request.user.student_groups:
                return True

            # if the user is a teacher from the same department, allow read
            if obj.department in request.user.teaching_departments:
                return True

        return False


class TeachingUnitPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: TeachingUnit) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the teaching unit department is managed by the user, allow all
        if obj.department in request.user.managing_departments:
            return True

        # if the teaching unit is managed by the user, allow all
        if obj in request.user.managing_units:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the user is related to the department, allow read
            if obj.department in request.user.related_departments:
                return True

        return False


class StudentCardPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: StudentCard) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the card department is managed by the user, allow all
        if obj.department in request.user.managing_departments:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the owner of the card is the user, allow read
            if obj.owner is request.user:
                return True

        return False


class TeachingSessionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: TeachingSession) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the teacher is the user, allow all
        if obj.teacher is request.user:
            return True

        # if the unit of the session is managed by the user, allow all
        if obj.unit in request.user.managing_units:
            return True

        # if the department of the session is managed by the user, allow all
        if obj.unit.department in request.user.managing_departments:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the user was one of the student, allow read
            if request.user in obj.group.students:
                return True

        return False


class AttendancePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Attendance) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the teacher is the user, allow all
        if obj.session.teacher is request.user:
            return True

        # if the unit of the session is managed by the user, allow all
        if obj.session.unit in request.user.managing_units:
            return True

        # if the department of the session is managed by the user, allow all
        if obj.session.unit.department in request.user.managing_departments:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the user was the student, allow read
            if obj.student is request.user:
                return True

        return False


class AbsencePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Absence) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the department of the session is managed by the user, allow all
        if obj.session.unit.department in request.user.managing_departments:
            return True

        # if the user was the student, allow all
        if obj.student is request.user:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the unit of the session is managed by the user, allow read
            if obj.session.unit in request.user.managing_units:
                return True

            # if the teacher is the user, allow read
            if obj.session.teacher is request.user:
                return True

        return False


class AbsenceAttachmentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: AbsenceAttachment) -> bool:
        # if the requesting user is admin, allow all
        if request.user.is_superuser:
            return True

        # if the department of the session is managed by the user, allow all
        if obj.absence.session.unit.department in request.user.managing_departments:
            return True

        # if the user was the student, allow all
        if obj.absence.student is request.user:
            return True

        if request.method in permissions.SAFE_METHODS:
            # if the unit of the session is managed by the user, allow read
            if obj.absence.session.unit in request.user.managing_units:
                return True

            # if the teacher is the user, allow read
            if obj.absence.session.teacher is request.user:
                return True

        return False
