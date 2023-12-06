"""
Models for the Palto project.

Models are the class that represent and abstract the database.
"""
import operator
import uuid
from abc import abstractmethod
from datetime import datetime, timedelta
from functools import reduce
from typing import Iterable

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet, Q, F


# TODO(Raphaël): split permissions from models for readability
# TODO(Raphaël): allow other function for permissions than in


class ModelPermissionHelper:
    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        """
        Return True if the user can create a new instance of this object
        """
        
        return user.is_superuser

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        """
        Return the list of fields in that model that the user can modify
        """

        return {}

    @classmethod
    @abstractmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        """
        Return True if the user can edit this object
        """

    @classmethod
    @abstractmethod
    def all_visible_by_user(cls, user: "User") -> QuerySet:
        """
        Return True if the user can see this object
        """


class User(AbstractUser, ModelPermissionHelper):
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

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        # if the user is managing a department, allow him to create user
        if user.managing_departments.count() > 0:
            return True

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        queryset = QuerySet()

        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            # all the users related to a department the user is managing
            if user.managing_departments.count() > 0:
                queryset = cls.objects.all()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            # if the user is in one of the same department as the requesting user
            queryset = Department.multiple_related_users(user.related_departments)

        return queryset.order_by("pk")


class Department(models.Model, ModelPermissionHelper):
    """
    A scholar department.

    For example, a same server can handle both a science department and a sport department.
    ALl have their own managers, teachers and student.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=64, unique=True)
    email: str = models.EmailField()

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

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        return user.is_superuser

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the manager of the department
                managers=user,
            )

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        # everybody can see all the departments
        queryset = cls.objects.all()

        return queryset.order_by("pk")


class StudentGroup(models.Model, ModelPermissionHelper):
    """
    A student group.

    This make selecting multiple students with a specificity easier.

    For example, if students are registered to an English course,
    putting them in a same group make them easier to select.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    name: str = models.CharField(max_length=128)

    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="owning_groups")
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, related_name="student_groups")
    students = models.ManyToManyField(to=get_user_model(), blank=True, related_name="student_groups")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} name={self.name!r}>"

    def __str__(self):
        return self.name

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        # if the user is managing a department
        if user.managing_departments.count() > 0:
            return True

        # if the user is teaching a department
        if user.teaching_departments.count() > 0:
            return True

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        # if the user is admin, no contrains
        if user.is_superuser:
            return {}

        return {
            # the managers and teachers can only interact with their departments
            "department": (user.managing_departments | user.teaching_departments).distinct()
        }

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the owner of the group, allow write
                Q(owner=user) |
                # if the user is a department manager, allow write
                Q(department__managers=user)
            ).distinct()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the owner of the group, allow read
                Q(owner=user) |
                # if the user is one of the student, allow read
                Q(students=user) |
                # if the user is a department manager, allow read
                Q(department__managers=user) |
                # if the user is one of the teachers, allow read
                Q(department__teachers=user)
            ).distinct()

        return queryset.order_by("pk")


class TeachingUnit(models.Model, ModelPermissionHelper):
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

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        # if the user is managing a department
        if user.managing_departments.count() > 0:
            return True

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        # if the user is admin, no contrains
        if user.is_superuser:
            return {}

        return {
            # the managers can only interact with their departments
            "department": user.managing_departments
        }

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is a manager of the department, allow write
                Q(department__managers=user) |
                # if the user is the manager of the unit, allow write
                Q(managers=user)
            ).distinct()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is a manager of the department, allow read
                Q(department__managers=user) |
                # if the user is the manager of the unit, allow read
                Q(managers=user) |
                # if the department is related to the user, allow read
                Q(department=user.related_departments)
            ).distinct()

        return queryset.order_by("pk")


class StudentCard(models.Model, ModelPermissionHelper):
    """
    A student card.

    This represents a student NFC card.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    uid: bytes = models.BinaryField(max_length=7)

    department: Department = models.ForeignKey(to=Department, on_delete=models.CASCADE, related_name="student_cards")
    owner: User = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="student_cards")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} owner={self.owner.username!r}>"

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        if user.managing_departments.count() > 0:
            return True

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        # if the user is admin, no contrains
        if user.is_superuser:
            return {}

        return {
            # the managers can only interact with their departments
            "department": user.managing_departments,
            # the owner of the card can be any students in a department that is managed by the user
            "owner": reduce(
                operator.or_,
                (department.students.all() for department in user.managing_departments)
            )
        }

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is a manager of the department
                Q(department__managers=user)
            ).distinct()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the owner
                Q(owner=user) |
                # if the user is a manager of the department
                Q(department__managers=user)
            ).distinct()

        return queryset.order_by("pk")


class TeachingSession(models.Model, ModelPermissionHelper):
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

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        # if the user is managing a department
        if user.managing_departments.count() > 0:
            return True

        # if the user is managing a unit
        if user.managing_units.count() > 0:
            return True

        # if the user is teaching a unit
        if user.teaching_units.count() > 0:
            return True

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        # if the user is admin, no contrains
        if user.is_superuser:
            return {}

        return {
            # the managers can only interact with their departments
            "department": (user.managing_departments | user.teaching_departments).distinct(),
            "teacher":
                # the teacher can be any teacher in a department that the user is managing
                reduce(
                    operator.or_,
                    (department.teachers.all() for department in user.managing_departments)
                ) | reduce(
                    # or a teacher in a unit that the user is managing
                    operator.or_,
                    (department.teachers.all() for department in user.managing_units)
                ) | (
                    # or the user itself
                    User.objects.filter(pk=user.pk)
                ),
            "unit":
                # the unit can be any unit in the department that the user is managing
                reduce(
                    operator.or_,
                    (department.teaching_units.all() for department in user.managing_departments)
                ) | (
                    # or the units that the user is teaching
                    user.teaching_sessions
                ),
            "group":
                # any group of a department where the user is a manager
                reduce(
                    operator.or_,
                    (department.student_groups for department in user.managing_departments)
                ) |
                # any group where the user is a manager or a teacher of a unit
                reduce(
                    operator.or_,
                    (unit.student_groups for unit in (user.managing_units | user.teaching_units))
                )
        }

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the teacher, allow write
                Q(teacher=user) |
                # if the user is managing the unit, allow write
                Q(unit__managers=user) |
                # if the user is managing the department, allow write
                Q(unit__department__managers=user)
            ).distinct()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the teacher, allow read
                Q(teacher=user) |
                # if the user is managing the unit, allow read
                Q(unit__managers=user) |
                # if the user is managing the department, allow read
                Q(unit__department__managers=user) |
                # if the user is part of the group, allow read
                Q(group__students=user)
            ).distinct()

        return queryset.order_by("pk")


class Attendance(models.Model, ModelPermissionHelper):
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

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        # if the user is managing a department
        if user.managing_departments.count() > 0:
            return True

        # if the user is managing a unit
        if user.managing_units.count() > 0:
            return True

        # if the user is teaching a unit
        if user.teaching_units.count() > 0:
            return True

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        # if the user is admin, no contrains
        if user.is_superuser:
            return {}

        return {
            # the managers can only interact with their departments
            "department": user.managing_departments | user.teaching_departments,
            "student":
                # student can be any student from a department the user is managing or teaching
                reduce(
                    operator.or_,
                    (
                        department.students.all() 
                        for department in (user.managing_departments | user.teaching_departments)
                    )
                ) |
                # or any student from a unit the user is managing or teaching
                reduce(
                    operator.or_,
                    (
                        student_group.students.all()
                        for unit in (user.managing_units | user.teaching_units)
                        for student_group in unit.student_groups
                    )
                ),
            "session":
                # the session can be any session where the user is managing the department
                reduce(
                    operator.or_,
                    (
                        unit.sessions
                        for department in user.managing_departments
                        for unit in department.teaching_units
                    )
                ) |
                # or where is the user is a teacher
                reduce(
                    operator.or_,
                    (
                        unit.sessions
                        for unit in (user.teaching_units | user.managing_units)
                    )
                )
        }

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user was the teacher, allow write
                Q(session__teacher=user) |
                # if the user is manager of the unit, allow write
                Q(session__unit__managers=user) |
                # if the user is manager of the department, allow write
                Q(session__unit__department__managers=user)
            ).distinct()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user was the teacher, allow read
                Q(session__teacher=user) |
                # if the user is manager of the unit, allow read
                Q(session__unit__managers=user) |
                # if the user is manager of the department, allow read
                Q(session__unit__department__managers=user) |

                # if the user is the student, allow read
                Q(student=user)
            ).distinct()

        return queryset.order_by("pk")


class Absence(models.Model, ModelPermissionHelper):
    """
    A student justified absence to a session.

    When a student signal his absence to a session, this is represented by this model.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    message: str = models.TextField()

    department: Department = models.ForeignKey(to=Department, on_delete=models.CASCADE, related_name="absences")
    student: User = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="absences")
    start: datetime = models.DateTimeField()
    end: datetime = models.DateTimeField()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"id={str(self.id)[:8]} "
            f"department={self.department} "
            f"student={self.student.username} "
            f"start={self.start} "
            f"end={self.end}"
            f">"
        )

    def __str__(self):
        return f"[{str(self.id)[:8]}] {self.student}"

    # properties

    def related_sessions(self) -> QuerySet[TeachingSession]:
        """
        Return the sessions that match the user absence
        """

        return TeachingSession.objects.filter(
            # every session where the student participate
            Q(group__students=self.student) &
            # every session that start between the start and the end of our absence
            Q(start__range=(self.start, self.end))
        ).distinct()

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        # if the user is a student
        if user.studying_departments.count() > 0:
            return True

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        # if the user is admin, no contrains
        if user.is_superuser:
            return {}

        return {
            # all the departments the user is studying in
            "department": user.studying_departments,
            # the student itself
            "student": User.objects.filter(pk=user.pk),
        }

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the student, allow write
                Q(student=user)
            ).distinct()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the student, allow read
                Q(student=user) |
                # if the user is related with the session, allow read
                (
                    # if the sessions start between the start and the end of the absence
                    Q(department__teaching_units__sessions__start__range=(F("start"), F("end"))) &
                    (
                        # the user is a manager of the department
                        Q(department__managers=user) |
                        # the user is a manager of the unit
                        Q(department__teaching_units__teachers=user) |
                        # the user is the teacher of the session
                        Q(department__teaching_units__sessions__teacher=user)
                    )
                )
            ).distinct()

        return queryset.order_by("pk")


class AbsenceAttachment(models.Model, ModelPermissionHelper):
    """
    An attachment to a student justified absence.

    The student can add additional files to justify his absence.
    """

    id: uuid.UUID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, max_length=36)
    content = models.FileField(upload_to="absence/attachment/")

    absence = models.ForeignKey(to=Absence, on_delete=models.CASCADE, related_name="attachments")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={str(self.id)[:8]} content={self.content!r}>"

    # permissions

    @classmethod
    def can_user_create(cls, user: "User") -> bool:
        # if the requesting user is admin
        if user.is_superuser:
            return True

        # if the user is a student
        if user.objects.count():
            return True

    @classmethod
    def user_fields_contrains(cls, user: "User") -> dict[str, QuerySet]:
        # if the user is admin, no contrains
        if user.is_superuser:
            return {}

        return {
            # all the departments the user is studying in
            "absence": user.absences,
        }

    @classmethod
    def all_editable_by_user(cls, user: "User") -> QuerySet:
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the student, allow write
                Q(absence__student=user)
            ).distinct()

        return queryset.order_by("pk")

    @classmethod
    def all_visible_by_user(cls, user: "User"):
        if user.is_superuser:
            # if the requesting user is admin
            queryset = cls.objects.all()
        else:
            queryset = cls.objects.filter(
                # if the user is the student, allow read
                Q(absence__student=user) |
                # if the user is related with the session, allow read
                (
                    # if the sessions start between the start and the end of the absence
                    Q(absence__department__teaching_units__sessions__start__range=(F("start"), F("end"))) &
                    (
                        # the user is a manager of the department
                        Q(absence__department__managers=user) |
                        # the user is a manager of the unit
                        Q(absence__department__teaching_units__teachers=user) |
                        # the user is the teacher of the session
                        Q(absence__department__teaching_units__sessions__teacher=user)
                    )
                )
            ).distinct()

        return queryset.order_by("pk")
