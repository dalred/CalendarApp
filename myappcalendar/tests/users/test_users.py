from users.models import User
from users.serializers import UserCreateSerializer, UserCurrentSerializer
from rest_framework.test import APIClient
from django.test import TestCase
from faker import Faker
from tests.factories import UserFactory

class Test_users(TestCase):
    """
        Test Users
    """
    def setUp(self):
        self.testuser = UserFactory(
            username="test1@example.com"
        )
        self.client = APIClient()  # APIClient(enforce_csrf_checks=True)
        self.faker = Faker()

    def test_check_user_create_serializer_data(self):
        username = self.faker.user_name()
        data = {
            "username": username,
            "password": "test",
            "password_repeat": "test",
        }

        response = self.client.post("/core/signup/", data=data)
        # Check PostData from Any
        expected_response = {
            "id": User.objects.last().pk,
            "username": username,
            "first_name": "Unknown",
            "last_name": "Unknown",
            "email": None
        }
        serializer = UserCreateSerializer(data=data)  # (Десерилизация Json→ dict)
        self.assertEqual(response.json(), expected_response)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_profile_user_data(self):
        self.client.force_login(user=self.testuser)
        response = self.client.get("/core/profile/", content_type='application/json')
        assert response.json() == UserCurrentSerializer(self.testuser).data  # Object -> OrderedDict (сериализация)

    def test_delete_user(self):
        self.client.force_login(user=self.testuser)
        response = self.client.delete("/core/profile/", content_type='application/json')
        assert response.status_code == 204