"""
Views for the Palto project's API v1.

An API view describe which models should display which files to user with which permissions.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import permissions
from . import serializers
from ... import models


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, permissions.UserPermission]

    def get_queryset(self):
        return models.User.all_visible_by_user(self.request.user)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [permissions.DepartmentPermission]

    def get_queryset(self):
        return models.Department.all_visible_by_user(self.request.user)


class StudentGroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentGroupSerializer
    permission_classes = [IsAuthenticated, permissions.StudentGroupPermission]

    def get_queryset(self):
        return models.StudentGroup.all_visible_by_user(self.request.user)


class TeachingUnitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeachingUnitSerializer
    permission_classes = [IsAuthenticated, permissions.TeachingUnitPermission]

    def get_queryset(self):
        return models.TeachingUnit.all_visible_by_user(self.request.user)


class StudentCardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentCardSerializer
    permission_classes = [IsAuthenticated, permissions.StudentCardPermission]

    def get_queryset(self):
        return models.StudentCard.all_visible_by_user(self.request.user)


class TeachingSessionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeachingSessionSerializer
    permission_classes = [IsAuthenticated, permissions.TeachingSessionPermission]

    def get_queryset(self):
        return models.TeachingSession.all_visible_by_user(self.request.user)


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AttendanceSerializer
    permission_classes = [IsAuthenticated, permissions.AttendancePermission]

    def get_queryset(self):
        return models.Attendance.all_visible_by_user(self.request.user)


class AbsenceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AbsenceSerializer
    permission_classes = [IsAuthenticated, permissions.AbsencePermission]

    def get_queryset(self):
        return models.Absence.all_visible_by_user(self.request.user)


class AbsenceAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AbsenceAttachmentSerializer
    permission_classes = [IsAuthenticated, permissions.AbsenceAttachmentPermission]

    def get_queryset(self):
        return models.AbsenceAttachment.all_visible_by_user(self.request.user)
