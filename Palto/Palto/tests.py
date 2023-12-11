"""
Tests for the Palto project.

Tests allow to easily check after modifying the logic behind a feature that everything still work as intended.
"""

from django import test

from Palto.Palto import factories


# Create your tests here.
class UserTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeUserFactory()


class DepartmentTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeDepartmentFactory()


class StudentGroupTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeStudentGroupFactory()


class TeachingUnitTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeTeachingUnitFactory()


class StudentCardTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeStudentCardFactory()


class TeachingSessionTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeTeachingSessionFactory()


class AttendanceTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeAttendanceFactory()


class AbsenceTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeAbsenceFactory()


class AbsenceAttachmentTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        factories.FakeAbsenceAttachmentFactory()
