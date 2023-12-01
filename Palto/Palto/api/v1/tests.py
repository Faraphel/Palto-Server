"""
Tests for the Palto project's API v1.

Everything to test the API v1 is described here.
"""

from django import test

from Palto.Palto import models, factories


class UserTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of users
        """

        user = factories.FakeUserFactory()


class DepartmentTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of departments
        """

        department = factories.FakeDepartmentFactory()


class StudentGroupTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of student groups
        """

        student_group = factories.FakeStudentGroupFactory()


class TeachingUnitTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of teaching units
        """

        teaching_unit = factories.FakeTeachingUnitFactory()


class StudentCardTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of student cards
        """

        student_card = factories.FakeStudentCardFactory()


class TeachingSessionTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of teaching sessions
        """

        teaching_session = factories.FakeTeachingSessionFactory()


class AttendanceTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of attendances
        """

        attendance = factories.FakeAttendanceFactory()


class AbsenceTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of absences
        """

        absence = factories.FakeAbsenceFactory()


class AbsenceAttachmentTestCase(test.TestCase):
    @staticmethod
    def test_creation():
        """
        Test the creation of absence attachments
        """

        absence_attachment = factories.FakeAbsenceAttachmentFactory()
