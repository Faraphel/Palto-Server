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
    queryset = models.User.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.UserPermission]


class DepartmentViewSet(UserViewSet):
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.all().order_by("pk")
    permission_classes = [permissions.DepartmentPermission]


class StudentGroupViewSet(UserViewSet):
    serializer_class = serializers.StudentGroupSerializer
    queryset = models.StudentGroup.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.StudentGroupPermission]


class TeachingUnitViewSet(UserViewSet):
    serializer_class = serializers.TeachingUnitSerializer
    queryset = models.TeachingUnit.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.TeachingUnitPermission]


class StudentCardViewSet(UserViewSet):
    serializer_class = serializers.StudentCardSerializer
    queryset = models.StudentCard.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.StudentCardPermission]


class TeachingSessionViewSet(UserViewSet):
    serializer_class = serializers.TeachingSessionSerializer
    queryset = models.TeachingSession.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.TeachingSessionPermission]


class AttendanceViewSet(UserViewSet):
    serializer_class = serializers.AttendanceSerializer
    queryset = models.Attendance.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.AttendancePermission]


class AbsenceViewSet(UserViewSet):
    serializer_class = serializers.AbsenceSerializer
    queryset = models.Absence.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.AbsencePermission]


class AbsenceAttachmentViewSet(UserViewSet):
    serializer_class = serializers.AbsenceAttachmentSerializer
    queryset = models.AbsenceAttachment.objects.all().order_by("pk")
    permission_classes = [IsAuthenticated, permissions.AbsenceAttachmentPermission]
