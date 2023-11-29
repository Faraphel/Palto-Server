import uuid
from abc import abstractmethod, ABC
from datetime import datetime, timedelta
from typing import Iterable

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet, Q
from rest_framework import permissions


# Create your models here.
class ModelApiMixin(ABC):
    @classmethod
    @abstractmethod
    def all_visible_to(cls, user: "User") -> QuerySet:
        """
        Return all the objects visible to a user.
        """

    @classmethod
    @abstractmethod
    def permissions_for(cls, user: "User", method: str) -> permissions.BasePermission:
        """
        Return the permissions for a user and the method used to access the object.
        """


class User(AbstractUser, ModelApiMixin):
    """
    A user.

    Same as the base Django user, but the id is now an uuid instead of an int.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} username={self.username!r}>"

    @staticmethod
    def multiple_related_departments(users: Iterable["User"]) -> QuerySet["Department"]:
        """
        Return all the related departments from multiple users.
        """

        return Department.objects.filter(
            Q(managers__in=users) |
            Q(teachers__in=users) |
            Q(students__in=users)
        ).distinct()

    @property
    def related_departments(self) -> QuerySet["Department"]:
        """
        The list of departments related with the user.
        """

        return self.multiple_related_departments([self])

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = User.objects.all()
        else:
            queryset = Department.multiple_related_users(user.related_departments)

        return queryset.order_by("pk")

    @classmethod
    def permissions_for(cls, user: "User", method: str) -> permissions.BasePermission:
        # TODO: ???
        if method in permissions.SAFE_METHODS:
            return permissions.AllowAny()

        return permissions.IsAdminUser()


class Department(models.Model, ModelApiMixin):
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

    @staticmethod
    def multiple_related_users(departments: Iterable["Department"]) -> QuerySet["User"]:
        """
        Return all the related users from multiple departments.
        """

        return User.objects.filter(
            Q(managing_departments__in=departments) |
            Q(teaching_departments__in=departments) |
            Q(studying_departments__in=departments)
        ).distinct()

    @property
    def related_users(self) -> QuerySet["User"]:
        """
        The list of users related with the department.
        """

        return self.multiple_related_users([self])

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        return cls.objects.all().order_by("pk")


class StudentGroup(models.Model, ModelApiMixin):
    """
    A student group.

    This make selecting multiple students with a specificity easier.

    For example, if students are registered to an English course,
    putting them in a same group make them easier to select.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=128)

    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, related_name="student_groups")
    students = models.ManyToManyField(to=get_user_model(), blank=True, related_name="student_groups")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} name={self.name!r}>"

    def __str__(self):
        return self.name

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = cls.objects.all()

        else:
            queryset = cls.objects.filter(
                # get all the groups where the user is
                Q(students=user) |
                # get all the groups where the department is managed by the user
                Q(department=user.managing_departments)
                # TODO: prof ? rôle créateur du groupe ?
            ).distinct()

        return queryset.order_by("pk")


class TeachingUnit(models.Model, ModelApiMixin):
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

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = cls.objects.all()

        else:
            queryset = cls.objects.filter(
                # get all the units with a common department with the user
                Q(department__in=user.related_departments)
            )

        return queryset.order_by("pk")


class StudentCard(models.Model, ModelApiMixin):
    """
    A student card.

    This represents a student NFC card.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    uid: bytes = models.BinaryField(max_length=7)

    owner: User = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="student_cards")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} owner={self.owner.username!r}>"

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = cls.objects.all()

        else:
            queryset = cls.objects.filter(
                # get all the cards that are owned by the user
                Q(owner=user) |
                # get all the cards where the owner is studying in a department where the user is a manager
                Q(owner__studying_departments__managers=user)
            ).distinct()

        return queryset.order_by("pk")


class TeachingSession(models.Model, ModelApiMixin):
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

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = cls.objects.all()

        else:
            queryset = cls.objects.filter(
                # get all the sessions where the user is a teacher
                Q(teacher=user) |
                # get all the sessions where the user is in the group
                Q(group__students=user) |
                # get all the sessions where the user is managing the unit
                Q(unit__managers=user) |
                # get all the sessions where the user is managing the department
                Q(unit__department__managers=user)
            ).distinct()

        return queryset.order_by("pk")


class Attendance(models.Model, ModelApiMixin):
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

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = cls.objects.all()

        else:
            queryset = cls.objects.filter(
                # get all the session where the user was the teacher
                Q(session__teacher=user) |
                # get all the session where the user was the student
                Q(student=user) |
                # get all the sessions where the user is managing the unit
                Q(session__unit__managers=user) |
                # get all the sessions where the user is managing the department
                Q(session__unit__department__managers=user)
            ).distinct()

        return queryset.order_by("pk")


class Absence(models.Model, ModelApiMixin):
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

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = cls.objects.all()

        else:
            queryset = cls.objects.filter(
                # get all the absence where the user was the teacher
                Q(session__teacher=user) |
                # get all the absence where the user was the student
                Q(student=user) |
                # get all the absences where the user is managing the unit
                Q(session__unit__managers=user) |
                # get all the absences where the user is managing the department
                Q(session__unit__department__managers=user)
            ).distinct()

        return queryset.order_by("pk")


class AbsenceAttachment(models.Model, ModelApiMixin):
    """
    An attachment to a student justified absence.

    The student can add additional files to justify his absence.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    content = models.FileField(upload_to="absence/attachment/")

    absence = models.ForeignKey(to=Absence, on_delete=models.CASCADE, related_name="attachments")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} content={self.content!r}>"

    @classmethod
    def all_visible_to(cls, user: "User") -> QuerySet["User"]:
        if user.is_superuser:
            queryset = cls.objects.all()

        else:
            queryset = cls.objects.filter(
                # get all the absence attachments where the user was the teacher
                Q(absence__session__teacher=user) |
                # get all the absence attachments where the user was the student
                Q(absence__student=user) |
                # get all the absence attachments where the user is managing the unit
                Q(absence__session__unit__managers=user) |
                # get all the absence attachments where the user is managing the department
                Q(absence__session__unit__department__managers=user)
            ).distinct()

        return queryset.order_by("pk")
