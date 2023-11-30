"""
Views for the Palto project's API v1.

An API view describe which models should display which files to user with which permissions.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import (UserPermission, DepartmentPermission, StudentGroupPermission, TeachingUnitPermission,
                          StudentCardPermission, TeachingSessionPermission, AttendancePermission, AbsencePermission,
                          AbsenceAttachmentPermission)
from .serializers import (UserSerializer, AbsenceAttachmentSerializer, AbsenceSerializer, AttendanceSerializer,
                          TeachingSessionSerializer, StudentCardSerializer, StudentGroupSerializer,
                          DepartmentSerializer, TeachingUnitSerializer)
from ...models import (User, AbsenceAttachment, Absence, Attendance, TeachingSession, StudentCard, TeachingUnit,
                       StudentGroup, Department)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserPermission]


class DepartmentViewSet(UserViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = [DepartmentPermission]


class StudentGroupViewSet(UserViewSet):
    serializer_class = StudentGroupSerializer
    queryset = StudentGroup.objects.all()
    permission_classes = [IsAuthenticated, StudentGroupPermission]


class TeachingUnitViewSet(UserViewSet):
    serializer_class = TeachingUnitSerializer
    queryset = TeachingUnit.objects.all()
    permission_classes = [IsAuthenticated, TeachingUnitPermission]


class StudentCardViewSet(UserViewSet):
    serializer_class = StudentCardSerializer
    queryset = StudentCard.objects.all()
    permission_classes = [IsAuthenticated, StudentCardPermission]


class TeachingSessionViewSet(UserViewSet):
    serializer_class = TeachingSessionSerializer
    queryset = TeachingSession.objects.all()
    permission_classes = [IsAuthenticated, TeachingSessionPermission]


class AttendanceViewSet(UserViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated, AttendancePermission]


class AbsenceViewSet(UserViewSet):
    serializer_class = AbsenceSerializer
    queryset = Absence.objects.all()
    permission_classes = [IsAuthenticated, AbsencePermission]


class AbsenceAttachmentViewSet(UserViewSet):
    serializer_class = AbsenceAttachmentSerializer
    queryset = AbsenceAttachment.objects.all()
    permission_classes = [IsAuthenticated, AbsenceAttachmentPermission]
