"""
Tests for the Palto project's API v1.

Everything to test the API v1 is described here.
"""

from rest_framework import status
from rest_framework import test

from Palto.Palto import factories, models
from Palto.Palto.api.v1 import serializers


class TokenJwtTestCase(test.APITestCase):
    """
    Test the JWT token creation
    """


class UserApiTestCase(test.APITestCase):
    # fake user data for creations test
    USER_CREATION_DATA: dict = {
        "username": "billybob",
        "first_name": "Billy",
        "last_name": "Bob",
        "email": "billy.bob@billybob.fr"
    }

    def setUp(self):
        self.user_admin = factories.FakeUserFactory(is_superuser=True)
        self.user_other = factories.FakeUserFactory()

    def test_permission_admin(self):
        """ Test the API permission for an administrator """

        # TODO: use reverse to get the url ?
        self.client.force_login(self.user_admin)

        # check for a get request
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], models.User.objects.count())

        # check for a post request
        response = self.client.post("/api/v1/users/", data=self.USER_CREATION_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_permission_anonymous(self):
        """ Test the API permission for an anonymous user """

        # TODO: use reverse to get the url ?
        self.client.logout()

        # check for a get request
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for a post request
        response = self.client.post("/api/v1/users/", data=self.USER_CREATION_DATA)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_unrelated(self):
        """ Test the API permission for an unrelated user """

        # TODO: use reverse to get the url ?
        self.client.force_login(self.user_other)

        # check for a get request and that he can't see anybody
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 0)

        # check for a post request
        response = self.client.post("/api/v1/users/", data=self.USER_CREATION_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_related(self):
        """ Test the API permission for a related user """

        # TODO: use reverse to get the url ?
        student1, student2 = factories.FakeUserFactory(), factories.FakeUserFactory()
        department = factories.FakeDepartmentFactory(students=(student1, student2))

        self.client.force_login(student1)

        # check for a get request and that he can see the other student
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializers.UserSerializer(student2).data, response.json()["results"])

        # check for a post request
        response = self.client.post("/api/v1/users/", data=self.USER_CREATION_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DepartmentApiTestCase(test.APITestCase):
    # fake department creation test
    DEPARTMENT_CREATION_DATA: dict = {
        "name": "UFR des Sciences",
        "email": "ufr.sciences@university.fr",
    }

    def setUp(self):
        self.user_admin = factories.FakeUserFactory(is_superuser=True)
        self.user_other = factories.FakeUserFactory()

    def test_permission_admin(self):
        """ Test the API permission for an administrator """

        # TODO: use reverse to get the url ?
        self.client.force_login(self.user_admin)

        # check for a get request
        response = self.client.get("/api/v1/departments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], models.Department.objects.count())

        # check for a post request
        response = self.client.post("/api/v1/departments/", data=self.DEPARTMENT_CREATION_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudentGroupApiTestCase(test.APITestCase):
    def setUp(self):
        self.user_admin = factories.FakeUserFactory(is_superuser=True)
        self.user_other = factories.FakeUserFactory()

        # fake group creation data
        self.test_manager_related = factories.FakeUserFactory()
        self.test_manager_other = factories.FakeUserFactory()

        self.test_teacher_owner = factories.FakeUserFactory()
        self.test_teacher_other = factories.FakeUserFactory()

        self.test_students_group = [factories.FakeUserFactory() for _ in range(10)]
        self.test_students_other = [factories.FakeUserFactory() for _ in range(10)]

        self.test_department = factories.FakeDepartmentFactory(
            managers=[self.test_manager_related],
            teachers=[self.test_teacher_owner, self.test_teacher_other],
            students=[*self.test_students_group, *self.test_students_other],
        )

        self.student_group_creation_data: dict = {
            "name": "Groupe 1",
            "owner": self.test_teacher_owner.pk,
            "department": self.test_department.pk,
            "students": map(lambda obj: obj.pk, self.test_students_group)
        }

    def test_permission_admin(self):
        """ Test the API permission for an administrator """

        # TODO: use reverse to get the url ?
        self.client.force_login(self.user_admin)

        # check for a get request
        response = self.client.get("/api/v1/student_groups/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], models.StudentGroup.objects.count())

        # check for a post request
        response = self.client.post("/api/v1/student_groups/", data=self.student_group_creation_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_permission_anonymous(self):
        """ Test the API permission for an anonymous user """

        # TODO: use reverse to get the url ?
        self.client.logout()

        # check for a get request
        response = self.client.get("/api/v1/student_groups/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for a post request
        response = self.client.post("/api/v1/student_groups/", data=self.student_group_creation_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
