"""
Factories for the Palto project.

Factories are class that allow for the automatic creation of instances of our models, primarily for testing purpose.
"""
import random

import factory

from Palto.Palto import models


# TODO(Raphaël): Voir pour la cohérence


class FakeUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")


class FakeDepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Department

    name = factory.Faker("company")
    email = factory.Faker("company_email")

    managers = factory.RelatedFactoryList(
        FakeUserFactory,
        "managing_departments",
        size=lambda: random.randint(1, 3)
    )
    teachers = factory.RelatedFactoryList(
        FakeUserFactory,
        "teaching_departments",
        size=lambda: random.randint(1, 50)
    )
    students = factory.RelatedFactoryList(
        FakeUserFactory,
        "studying_departments",
        size=lambda: random.randint(1, 500)
    )


class FakeStudentGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentGroup

    name = factory.Faker("administrative_unit")

    owner = factory.SubFactory(FakeUserFactory)
    department = factory.SubFactory(FakeDepartmentFactory)
    students = factory.RelatedFactoryList(FakeUserFactory, "student_groups", size=lambda: random.randint(0, 32))


class FakeTeachingUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TeachingUnit

    name = factory.Faker("administrative_unit")

    department = factory.SubFactory(
        FakeDepartmentFactory
    )
    managers = factory.RelatedFactoryList(
        FakeUserFactory,
        "managing_units",
        size=lambda: random.randint(1, 3)
    )
    teachers = factory.RelatedFactoryList(
        FakeUserFactory,
        "teaching_units",
        size=lambda: random.randint(1, 5)
    )
    student_groups = factory.RelatedFactoryList(
        FakeStudentGroupFactory,
        "studying_units",
        size=lambda: random.randint(1, 3)
    )


class FakeStudentCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentCard

    uid = factory.Faker("binary", length=7)

    department = factory.SubFactory(FakeDepartmentFactory)
    owner = factory.SubFactory(FakeUserFactory)


class FakeTeachingSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TeachingSession

    start = factory.Faker("date_time")
    duration = factory.Faker("time_delta")
    note = factory.Faker("paragraph")

    unit = factory.SubFactory(FakeTeachingUnitFactory)

    group = factory.SubFactory(FakeStudentGroupFactory)
    owner = factory.SubFactory(FakeUserFactory)


class FakeAttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Attendance

    date = factory.Faker("date_time")

    student = factory.SubFactory(FakeUserFactory)
    session = factory.SubFactory(FakeTeachingSessionFactory)


class FakeAbsenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Absence

    message = factory.Faker("paragraph")

    student = factory.SubFactory(FakeUserFactory)
    session = factory.SubFactory(FakeTeachingSessionFactory)


class FakeAbsenceAttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AbsenceAttachment

    content = factory.django.FileField()

    absence = factory.SubFactory(FakeAbsenceFactory)
