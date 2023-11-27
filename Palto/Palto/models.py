import uuid
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Department(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=32)

    managers = models.ManyToManyField(to=get_user_model(), related_name="managed_departments")
    teachers = models.ManyToManyField(to=get_user_model(), related_name="taught_departments")
    students = models.ManyToManyField(to=get_user_model(), related_name="study_departments")


class StudentGroup(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=32)

    students = models.ManyToManyField(to=get_user_model(), related_name="student_groups")


class TeachingUnit(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=32)

    student_groups = models.ManyToManyField(to=StudentGroup, related_name="taught_units")


class StudentCard(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    uid: bytes = models.BinaryField(max_length=7)

    owner = models.ManyToManyField(to=get_user_model(), related_name="student_cards")


class TeachingSession(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    start: datetime = models.DateTimeField()
    duration: timedelta = models.DurationField()

    teacher = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="taught_sessions")

    @property
    def end(self) -> datetime:
        return self.start + self.duration


class Attendance(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    date: datetime = models.DateTimeField()

    student = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="attended_sessions")


class Absence(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    message: str = models.TextField()

    student = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="absent_sessions")


class AbsenceAttachment(models.Model):
    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    content = models.FileField()

    absence = models.ForeignKey(to=Absence, on_delete=models.CASCADE, related_name="attachments")
