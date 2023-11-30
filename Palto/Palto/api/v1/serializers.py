"""
Serializers for the Palto project's API v1.

A serializers tell the API how should a model should be serialized to be used by an external user.
"""

from rest_framework import serializers

from Palto.Palto import models


# TODO(Raphaël): Voir pour les related_name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = ['id', 'name', 'email', 'managers']
        # NOTE: teachers, students


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentGroup
        fields = ['id', 'name', 'owner', 'department']
        # NOTE: students


class TeachingUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeachingUnit
        fields = ['id', 'name', 'department']
        # NOTE: managers, teachers, student_groups


class StudentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentCard
        fields = ['id', 'uid', 'department', 'owner']


class TeachingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeachingSession
        fields = ['id', 'start', 'duration', 'note', 'unit', 'group', 'teacher']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attendance
        fields = ['id', 'date', 'student', 'session']


class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Absence
        fields = ['id', 'message', 'student', 'session']


class AbsenceAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AbsenceAttachment
        fields = ['id', 'content', 'absence']
