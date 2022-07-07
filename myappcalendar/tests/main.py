from rest_framework.test import APIClient
from django.test import TestCase
# pytest tests / -vv
# pytest tests/goals/ tests/users/ -vv
# pytest tests/main.py -vv
# pytest tests/users/test_users.py -vv
# pytest tests/users/test_users.py -vv -rx|-rP
# pytest tests/users/test_users.py::test_post_users -vv
from faker import Faker


class UseFactoryClassTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()  # APIClient(enforce_csrf_checks=True)
        self.faker = Faker()

    # def run_tests(self):
    #     test_retrieve_user(self.client)
