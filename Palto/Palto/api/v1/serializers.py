"""
Serializers for the Palto project's API v1.

A serializers tell the API how should a model should be serialized to be used by an external user.
"""
from typing import Type

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from Palto.Palto import models


# TODO: voir les relations inversées ?


class ModelSerializerContrains(serializers.ModelSerializer):
    """
    Similar to the base ModelSerializer, but automatically check for contrains for the user
    when trying to create a new instance or modifying a field.
    """

    class Meta:
        model: Type[models.ModelPermissionHelper]

    def create(self, validated_data):
        # get the fields that this user can modify
        field_contrains = self.Meta.model.user_fields_contraints(self.context["request"].user)

        # for every constraints
        for field, constraints in field_contrains.items():
            # check if the value is in the constraints.
            value = validated_data.get(field)
            if value is not None and value not in constraints:
                raise PermissionDenied(f"You are not allowed to use this value for the field {field}.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # get the fields that this user can modify
        field_contrains = self.Meta.model.user_fields_contraints(self.context["request"].user)

        # for every constraints
        for field, constraints in field_contrains.items():
            # check if the value of the request is in the constraints.
            value = validated_data.get(field)
            if value is not None and value not in constraints:
                raise PermissionDenied(f"You are not allowed to use this value for the field {field}.")

            # check if the value of the already existing instance is in the constraints.
            value = getattr(instance, field, None)
            if value is not None and value not in constraints:
                raise PermissionDenied(f"You are not allowed to use this value for the field {field}.")

        # check that the user is managing the department
        if instance.department not in self.context["request"].user.managing_departments:
            raise PermissionDenied("You don't manage this department.")

        return super().update(instance, validated_data)


class UserSerializer(ModelSerializerContrains):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class DepartmentSerializer(ModelSerializerContrains):
    class Meta:
        model = models.Department
        fields = ['id', 'name', 'email', 'managers', 'teachers', 'students']


class StudentGroupSerializer(ModelSerializerContrains):
    class Meta:
        model = models.StudentGroup
        fields = ['id', 'name', 'owner', 'department', 'students']


class TeachingUnitSerializer(ModelSerializerContrains):
    class Meta:
        model = models.TeachingUnit
        fields = ['id', 'name', 'department', 'managers', 'teachers', 'student_groups']


class StudentCardSerializer(ModelSerializerContrains):
    class Meta:
        model = models.StudentCard
        fields = ['id', 'uid', 'department', 'owner']


class TeachingSessionSerializer(ModelSerializerContrains):
    class Meta:
        model = models.TeachingSession
        fields = ['id', 'start', 'duration', 'note', 'unit', 'group', 'teacher']


class AttendanceSerializer(ModelSerializerContrains):
    class Meta:
        model = models.Attendance
        fields = ['id', 'date', 'student', 'session']


class AbsenceSerializer(ModelSerializerContrains):
    class Meta:
        model = models.Absence
        fields = ['id', 'message', 'student', 'session']


class AbsenceAttachmentSerializer(ModelSerializerContrains):
    class Meta:
        model = models.AbsenceAttachment
        fields = ['id', 'content', 'absence']
