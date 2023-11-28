import uuid
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    A user.

    Same as the base Django user, but the id is now an uuid instead of an int.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} username={self.username!r}>"


class Department(models.Model):
    """
    A scholar department.

    For example, a same server can handle both a science department and a sport department.
    ALl have their own managers, teachers and student.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=64)
    mail: str = models.EmailField()

    managers = models.ManyToManyField(to=get_user_model(), blank=True, related_name="managing_departments")
    teachers = models.ManyToManyField(to=get_user_model(), blank=True, related_name="teaching_departments")
    students = models.ManyToManyField(to=get_user_model(), blank=True, related_name="studying_departments")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} name={self.name!r}>"

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    """
    A student group.

    This make selecting multiple students with a specificity easier.

    For example, if students are registered to an English course,
    putting them in a same group make them easier to select.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=128)

    students = models.ManyToManyField(to=get_user_model(), blank=True, related_name="student_groups")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} name={self.name!r}>"

    def __str__(self):
        return self.name


class TeachingUnit(models.Model):
    """
    A teaching unit.

    This represents a unit that can be taught to groups of student.

    For example, Maths, English, French, Computer Science are all teaching units.
    The registered groups are groups of student allowed to participate in these units.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=64)

    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, related_name="teaching_units")

    managers = models.ManyToManyField(to=get_user_model(), blank=True, related_name="managing_units")
    teachers = models.ManyToManyField(to=get_user_model(), blank=True, related_name="teaching_units")
    student_groups = models.ManyToManyField(to=StudentGroup, blank=True, related_name="studying_units")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} name={self.name!r}>"

    def __str__(self):
        return self.name


class StudentCard(models.Model):
    """
    A student card.

    This represents a student NFC card.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    uid: bytes = models.BinaryField(max_length=7)

    owner: User = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="student_cards")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} owner={self.owner.username!r}>"


class TeachingSession(models.Model):
    """
    A session of a teaching unit.

    For example, a session of English would be a single course of this unit.

    It references a teacher responsible for scanning the student cards, student attendances and student absences.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    start: datetime = models.DateTimeField()
    duration: timedelta = models.DurationField()
    note: str = models.TextField(blank=True)

    unit = models.ForeignKey(to=TeachingUnit, on_delete=models.CASCADE, related_name="sessions")

    group = models.ForeignKey(to=StudentGroup, on_delete=models.CASCADE, related_name="teaching_sessions")
    teacher = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="teaching_sessions")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} unit={self.unit.name!r} start={self.start}>"

    def __str__(self):
        return f"{self.unit.name} ({self.start})"

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

    student: User = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="attended_sessions"
    )
    session: TeachingSession = models.ForeignKey(
        to=TeachingSession,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"id={str(self.id)[:8]} "
            f"student={self.student.username} "
            f"session={str(self.session.id)[:8]}"
            f">"
        )


class Absence(models.Model):
    """
    A student justified absence to a session.

    When a student signal his absence to a session, this is represented by this model.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    message: str = models.TextField()

    student: User = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="absented_sessions")
    session: TeachingSession = models.ManyToManyField(to=TeachingSession, blank=True, related_name="absences")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"id={str(self.id)[:8]} "
            f"student={self.student.username} "
            f"session={str(self.session.id)[:8]}"
            f">"
        )

    def __str__(self):
        return f"[{str(self.id)[:8]}] {self.student}"


class AbsenceAttachment(models.Model):
    """
    An attachment to a student justified absence.

    The student can add additional files to justify his absence.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    content = models.FileField(upload_to="absence/attachment/")

    absence = models.ForeignKey(to=Absence, on_delete=models.CASCADE, related_name="attachments")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} content={self.content!r}>"
