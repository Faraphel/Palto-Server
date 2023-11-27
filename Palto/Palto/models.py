import uuid
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Department(models.Model):
    """
    A scholar department.

    For example, a same server can handle both a science department and a sport department.
    ALl have their own managers, teachers and student.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=32)

    managers = models.ManyToManyField(to=get_user_model(), related_name="managed_departments")
    teachers = models.ManyToManyField(to=get_user_model(), related_name="taught_departments")
    students = models.ManyToManyField(to=get_user_model(), related_name="study_departments")


class StudentGroup(models.Model):
    """
    A student group.

    This make selecting multiple students with a specificity easier.

    For example, if students are registered to an English course,
    putting them in a same group make them easier to select.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=32)

    students = models.ManyToManyField(to=get_user_model(), related_name="student_groups")


class TeachingUnit(models.Model):
    """
    A teaching unit.

    This represents a unit that can be taught to groups of student.

    For example, Maths, English, French, Computer Science are all teaching units.
    The registered groups are groups of student allowed to participate in these units.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=32)

    student_groups = models.ManyToManyField(to=StudentGroup, related_name="taught_units")


class StudentCard(models.Model):
    """
    A student card.

    This represents a student NFC card.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    uid: bytes = models.BinaryField(max_length=7)

    owner = models.ManyToManyField(to=get_user_model(), related_name="student_cards")


class TeachingSession(models.Model):
    """
    A session of a teaching unit.

    For example, a session of English would be a single course of this unit.

    It references a teacher responsible for scanning the student cards, student attendances and student absences.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    start: datetime = models.DateTimeField()
    duration: timedelta = models.DurationField()

    teacher = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="taught_sessions")

    @property
    def end(self) -> datetime:
        return self.start + self.duration


class Attendance(models.Model):
    """
    A student attendance to a session.

    When a student confirm his presence to a session, this is represented by this model.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    date: datetime = models.DateTimeField()

    student = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="attended_sessions")


class Absence(models.Model):
    """
    A student justified absence to a session.

    When a student signal his absence to a session, this is represented by this model.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    message: str = models.TextField()

    student = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="absent_sessions")


class AbsenceAttachment(models.Model):
    """
    An attachment to a student justified absence.

    The student can add additional files to justify his absence.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    content = models.FileField()

    absence = models.ForeignKey(to=Absence, on_delete=models.CASCADE, related_name="attachments")
