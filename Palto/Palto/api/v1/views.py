"""
Views for the Palto project's API v1.

An API view describe which models should display which files to user with which permissions.
"""
from typing import Type

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.serializers import BaseSerializer

from . import permissions
from . import serializers
from ... import models


def view_from_helper_class(
        model_class: Type[models.ModelPermissionHelper],
        serializer_class: Type[BaseSerializer],
        permission_classes: list[Type[BasePermission]],
) -> Type[viewsets.ModelViewSet]:
    """
    Create a view class from a model if it implements ModelPermissionHelper.
    This make creating view easier to understand and less redundant.
    """

    class ViewSet(viewsets.ModelViewSet):
        nonlocal serializer_class, permission_classes, model_class

        def get_serializer_class(self):
            return serializer_class

        def get_permissions(self):
            return [permission() for permission in permission_classes]

        def get_queryset(self):
            return model_class.all_visible_by_user(self.request.user)

    return ViewSet


UserViewSet = view_from_helper_class(
    model_class=models.User,
    serializer_class=serializers.UserSerializer,
    permission_classes=[IsAuthenticated, permissions.UserPermission]
)
DepartmentViewSet = view_from_helper_class(
    model_class=models.Department,
    serializer_class=serializers.DepartmentSerializer,
    permission_classes=[IsAuthenticated, permissions.DepartmentPermission]
)
StudentGroupViewSet = view_from_helper_class(
    model_class=models.StudentGroup,
    serializer_class=serializers.StudentGroupSerializer,
    permission_classes=[IsAuthenticated, permissions.StudentGroupPermission]
)
TeachingUnitViewSet = view_from_helper_class(
    model_class=models.TeachingUnit,
    serializer_class=serializers.TeachingUnitSerializer,
    permission_classes=[IsAuthenticated, permissions.TeachingUnitPermission]
)
StudentCardViewSet = view_from_helper_class(
    model_class=models.StudentCard,
    serializer_class=serializers.StudentCardSerializer,
    permission_classes=[IsAuthenticated, permissions.StudentCardPermission]
)
TeachingSessionViewSet = view_from_helper_class(
    model_class=models.TeachingSession,
    serializer_class=serializers.TeachingSessionSerializer,
    permission_classes=[IsAuthenticated, permissions.TeachingSessionPermission]
)
AttendanceViewSet = view_from_helper_class(
    model_class=models.Attendance,
    serializer_class=serializers.AttendanceSerializer,
    permission_classes=[IsAuthenticated, permissions.AttendancePermission]
)
AbsenceViewSet = view_from_helper_class(
    model_class=models.Absence,
    serializer_class=serializers.AbsenceSerializer,
    permission_classes=[IsAuthenticated, permissions.AbsencePermission]
)
AbsenceAttachmentViewSet = view_from_helper_class(
    model_class=models.AbsenceAttachment,
    serializer_class=serializers.AbsenceAttachmentSerializer,
    permission_classes=[IsAuthenticated, permissions.AbsenceAttachmentPermission]
)
