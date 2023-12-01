"""
Factories for the Palto project.

Factories are class that allow for the automatic creation of instances of our models, primarily for testing purpose.
"""
import random
from datetime import datetime, timedelta

import factory
import faker
from django.utils import timezone

from Palto.Palto import models


fake = faker.Faker()


class FakeUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username: str = factory.Sequence(lambda obj: f"{fake.user_name()}{random.randint(1000, 9999)}")
    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    email: str = factory.Faker("email")


class FakeDepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Department

    name: str = factory.Faker("company")
    email: str = factory.Faker("company_email")

    @factory.post_generation
    def managers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.managers.add(*extracted)
        else:
            self.managers.add(*[FakeUserFactory() for _ in range(random.randint(1, 3))])

    @factory.post_generation
    def teachers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.teachers.add(*extracted)
        else:
            self.teachers.add(*[FakeUserFactory() for _ in range(random.randint(2, 10))])

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.students.add(*extracted)
        else:
            self.students.add(*[FakeUserFactory() for _ in range(random.randint(50, 150))])


class FakeStudentGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentGroup

    name: str = factory.Faker("administrative_unit")

    owner: models.User = factory.SubFactory(FakeUserFactory)
    department: models.Department = factory.SubFactory(FakeDepartmentFactory)

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.students.add(*extracted)
        else:
            # create a group of between 5 and 50 students from this department
            self.students.add(*self.department.students.order_by('?')[:random.randint(5, 50)])


class FakeTeachingUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TeachingUnit

    name: str = factory.Faker("administrative_unit")

    department: models.Department = factory.SubFactory(
        FakeDepartmentFactory
    )

    @factory.post_generation
    def managers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.managers.add(*extracted)
        else:
            # create a group of between 1 and 2 managers from the teacher's department
            self.managers.add(*self.department.teachers.order_by('?')[:random.randint(1, 2)])

    @factory.post_generation
    def teachers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.teachers.add(*extracted)
        else:
            # create a group of between 2 and 10 teachers from the teacher's department
            self.teachers.add(*self.department.teachers.order_by('?')[:random.randint(2, 10)])

    @factory.post_generation
    def student_groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.student_groups.add(*extracted)
        else:
            # create a group of between 1 and 2 student groups from the department
            self.student_groups.add(*[
                FakeStudentGroupFactory.create(department=self.department)
                for _ in range(random.randint(1, 2))
            ])


class FakeStudentCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentCard

    uid: bytes = factory.Faker("binary", length=7)

    department: models.Department = factory.SubFactory(FakeDepartmentFactory)
    owner: models.User = factory.SubFactory(FakeUserFactory)


class FakeTeachingSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TeachingSession

    start: timedelta = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    duration: timedelta = factory.Faker("time_delta")
    note: str = factory.Faker("paragraph")

    unit: models.TeachingUnit = factory.SubFactory(FakeTeachingUnitFactory)

    group: models.StudentGroup = factory.SubFactory(FakeStudentGroupFactory)
    teacher: models.User = factory.SubFactory(FakeUserFactory)


class FakeAttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Attendance

    date: datetime = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())

    student: models.User = factory.SubFactory(FakeUserFactory)
    session: models.TeachingSession = factory.SubFactory(FakeTeachingSessionFactory)


class FakeAbsenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Absence

    message: str = factory.Faker("paragraph")

    student: models.User = factory.SubFactory(FakeUserFactory)

    @factory.post_generation
    def sessions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is not None:
            self.sessions.add(*extracted)
        else:
            # all the sessions should be in the same department
            department = FakeDepartmentFactory()

            # create a group of between 1 and 8 sessions from the department
            self.sessions.add(*[
                FakeTeachingSessionFactory.create(unit__department=department)
                for _ in range(random.randint(1, 8))
            ])


class FakeAbsenceAttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AbsenceAttachment

    content = factory.django.FileField()

    absence = factory.SubFactory(FakeAbsenceFactory)
