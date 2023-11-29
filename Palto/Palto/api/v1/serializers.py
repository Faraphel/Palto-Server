from rest_framework import serializers

from Palto.Palto.models import (User, Department, TeachingUnit, StudentCard, TeachingSession, Attendance, Absence,
                                AbsenceAttachment, StudentGroup)


# TODO(Raphaël): Les champs sont-ils sûr ? (carte uid ?)
# TODO(Raphaël): Connection à l'API avec token ?
# TODO(Raphaël): Voir pour les relations


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'mail']


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ['id', 'name']


class TeachingUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingUnit
        fields = ['id', 'name', 'department']


class StudentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCard
        fields = ['id', 'uid', 'owner']


class TeachingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingSession
        fields = ['id', 'start', 'duration', 'note', 'unit', 'group', 'teacher']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'student']


class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = ['id', 'message', 'student']


class AbsenceAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceAttachment
        fields = ['id', 'content', 'absence']
