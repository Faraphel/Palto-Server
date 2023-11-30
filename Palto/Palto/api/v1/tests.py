"""
Tests for the Palto project's API v1.

Everything to test the API v1 is described here.
"""

from django import test

from Palto.Palto import models, factories


class UserTestCase(test.TestCase):
    @staticmethod
    def fake_factory():
        """
        Test the creation of fake users
        """

        for _ in range(100):
            factories.FakeUserFactory()


class DepartmentTestCase(test.TestCase):
    def creation(self):
        pass
