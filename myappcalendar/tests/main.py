from rest_framework.test import APIClient
from django.test import TestCase



# pytest tests / -vv
# pytest tests\users\test_users.py -vv
# pytest tests\users\test_users.py -vv -rx|-rP
# pytest tests\users\test_users.py::test_post_users -vv
class UseFactoryClassTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()