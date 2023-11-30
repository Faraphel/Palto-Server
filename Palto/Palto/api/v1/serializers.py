from rest_framework import serializers

from Palto.Palto.models import (User, Department, TeachingUnit, StudentCard, TeachingSession, Attendance, Absence,
                                AbsenceAttachment, StudentGroup)


# TODO(Raphaël): Voir pour les related_name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'email', 'managers']
        # NOTE: teachers, students


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ['id', 'name', 'owner', 'department']
        # NOTE: students


class TeachingUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingUnit
        fields = ['id', 'name', 'department']
        # NOTE: managers, teachers, student_groups


class StudentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCard
        fields = ['id', 'uid', 'department', 'owner']


class TeachingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingSession
        fields = ['id', 'start', 'duration', 'note', 'unit', 'group', 'teacher']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'student', 'session']


class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = ['id', 'message', 'student', 'session']


class AbsenceAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceAttachment
        fields = ['id', 'content', 'absence']
