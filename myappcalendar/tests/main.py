from rest_framework.test import APIClient
from django.test import TestCase
# pytest tests / -vv
# pytest tests/main.py -vv
# pytest tests/users/test_users.py -vv
# pytest tests/users/test_users.py -vv -rx|-rP
# pytest tests/users/test_users.py::test_post_users -vv
from tests.users.test_users import test_retrieve_user


class UseFactoryClassTestCase(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

    # def run_tests(self):
    #     test_retrieve_user(self.client)
