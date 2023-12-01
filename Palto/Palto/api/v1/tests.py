"""
Tests for the Palto project's API v1.

Everything to test the API v1 is described here.
"""

from rest_framework import status
from rest_framework import test

from Palto.Palto import factories


class TokenJwtTestCase(test.APITestCase):
    """
    Test the JWT token creation
    """


class UserApiTestCase(test.APITestCase):
    def setUp(self):
        self.user_admin = factories.FakeUserFactory(is_superuser=True)
        self.user_anonymous = factories.FakeUserFactory()

    def test_permission_admin(self):
        """ Test the permissions of the object for an admin """

        self.client.force_login(self.user_admin)

        # check for a get request
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for a post request
        response = self.client.post("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DepartmentApiTestCase(test.APITestCase):
    pass


class StudentGroupApiTestCase(test.APITestCase):
    pass


class TeachingUnitApiTestCase(test.APITestCase):
    pass


class StudentCardApiTestCase(test.APITestCase):
    pass


class TeachingSessionApiTestCase(test.APITestCase):
    pass


class AttendanceApiTestCase(test.APITestCase):
    pass


class AbsenceApiTestCase(test.APITestCase):
    pass


class AbsenceAttachmentApiTestCase(test.APITestCase):
    pass
