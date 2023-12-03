"""
Permissions for the Palto project's API v1.

A permission describe which user is allowed to see and modify which objet with the API
"""

from rest_framework import permissions

from Palto.Palto import models


class UserPermission(permissions.BasePermission):
    # TODO: has_permission check for authentication

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.User.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.User.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.User.all_editable_by_user(request.user)


class DepartmentPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.Department.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.Department.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.Department.all_editable_by_user(request.user)


class StudentGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.StudentGroup.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.StudentGroup.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.StudentGroup.all_editable_by_user(request.user)


class TeachingUnitPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.TeachingUnit.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.TeachingUnit.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.TeachingUnit.all_editable_by_user(request.user)


class StudentCardPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.StudentCard.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.StudentCard.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.StudentCard.all_editable_by_user(request.user)


class TeachingSessionPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.TeachingSession.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.TeachingSession.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.TeachingSession.all_editable_by_user(request.user)


class AttendancePermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.Attendance.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.Attendance.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.Attendance.all_editable_by_user(request.user)


class AbsencePermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.Absence.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.Absence.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.Absence.all_editable_by_user(request.user)


class AbsenceAttachmentPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, allow everybody
            return True

        if models.AbsenceAttachment.can_user_create(request.user):
            # for writing, only allowed users
            return True

        return False

    def has_object_permission(self, request, view, obj: models.User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # for reading, only allow if the user can see the object
            return obj in models.AbsenceAttachment.all_visible_by_user(request.user)

        else:
            # for writing, only allow if the user can edit the object
            return obj in models.AbsenceAttachment.all_editable_by_user(request.user)