"""
Permissions for the Palto project's API v1.

A permission describe which user is allowed to see and modify which objet with the API
"""

from typing import Type

from rest_framework import permissions

from Palto.Palto import models


def permission_from_helper_class(model: Type[models.ModelPermissionHelper]) -> Type[permissions.BasePermission]:
    """
    Create a permission class from a model if it implements ModelPermissionHelper.
    This make creating permission easier to understand and less redundant.
    """

    class Permission(permissions.BasePermission):
        def has_permission(self, request, view) -> bool:
            if request.method in permissions.SAFE_METHODS:
                # for reading, allow everybody
                return True

            if model.can_user_create(request.user):
                # for writing, only allowed users
                return True

            return False

        def has_object_permission(self, request, view, obj: models.User) -> bool:
            if request.method in permissions.SAFE_METHODS:
                # for reading, only allow if the user can see the object
                return obj in model.all_visible_by_user(request.user)

            else:
                # for writing, only allow if the user can edit the object
                return obj in model.all_editable_by_user(request.user)

    return Permission


UserPermission = permission_from_helper_class(models.User)
DepartmentPermission = permission_from_helper_class(models.Department)
StudentGroupPermission = permission_from_helper_class(models.StudentGroup)
TeachingUnitPermission = permission_from_helper_class(models.TeachingUnit)
StudentCardPermission = permission_from_helper_class(models.StudentCard)
TeachingSessionPermission = permission_from_helper_class(models.TeachingSession)
AttendancePermission = permission_from_helper_class(models.Attendance)
AbsencePermission = permission_from_helper_class(models.Absence)
AbsenceAttachmentPermission = permission_from_helper_class(models.AbsenceAttachment)
