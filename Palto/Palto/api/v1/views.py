from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserSerializer, AbsenceAttachmentSerializer, AbsenceSerializer, AttendanceSerializer,
                          TeachingSessionSerializer, StudentCardSerializer, StudentGroupSerializer,
                          DepartmentSerializer, TeachingUnitSerializer)
from ...models import (User, AbsenceAttachment, Absence, Attendance, TeachingSession, StudentCard, TeachingUnit,
                       StudentGroup, Department)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.all_visible_to(self.request.user)

    def get_permissions(self):
        return User.permissions_for(self.request.user, self.request.method)


class DepartmentViewSet(UserViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.all_visible_to(self.request.user)


class StudentGroupViewSet(UserViewSet):
    serializer_class = StudentGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentGroup.all_visible_to(self.request.user)


class TeachingUnitViewSet(UserViewSet):
    serializer_class = TeachingUnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeachingUnit.all_visible_to(self.request.user)


class StudentCardViewSet(UserViewSet):
    serializer_class = StudentCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentCard.all_visible_to(self.request.user)


class TeachingSessionViewSet(UserViewSet):
    serializer_class = TeachingSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeachingSession.all_visible_to(self.request.user)


class AttendanceViewSet(UserViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attendance.all_visible_to(self.request.user)


class AbsenceViewSet(UserViewSet):
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Absence.all_visible_to(self.request.user)


class AbsenceAttachmentViewSet(UserViewSet):
    serializer_class = AbsenceAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AbsenceAttachment.all_visible_to(self.request.user)
