import json
import pytest
import testit
from users.models import User
from users.serializers import UserCreateSerializer, UserCurrentSerializer
from rest_framework.test import APIClient
from django.test import TestCase
from faker import Faker
from tests.factories import UserFactory
import pprint

class Test_users(TestCase):
    """
        Test Users
    """

    def setUp(self):
        self.faker = Faker()
        self.testuser = UserFactory(
            username="test1@example.com",
        )
        self.password = self.faker.password(length=12)
        self.testuser.set_password(self.password)
        self.testuser.save()
        self.client = APIClient()  # APIClient(enforce_csrf_checks=True)

    def test_check_post_user_create_serializer_data(self):
        username = self.faker.user_name()
        password = self.password
        data = {
            "username": username,
            "password": password,
            "password_repeat": password,
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

    def test_post_login_user(self):
        password = self.password
        username = self.testuser.username
        data = {
            "username": username,
            "password": password,
        }
        response = self.client.post("/core/login/", data=data)
        expected_response = {
            "username": username,
            "password": password,
        }
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        self.client.force_login(user=self.testuser)
        response = self.client.delete("/core/profile/", content_type='application/json')
        assert response.status_code == 204

    def test_change_password(self):
        username = self.testuser.username
        old_password = self.password
        new_password = self.faker.password(length=12)
        # создаем нового пользователя так как не знаем старый пароль
        testuser = UserFactory(
            username=username,
            password=old_password
        )
        self.client.force_login(user=testuser)
        data = {
            "old_password": old_password,
            "new_password": new_password
        }
        response = self.client.put("/core/update_password/", data=data)
        # проверяем только на статус код так как 201 no content по идее не должен что-то возвращать
        # внесли изменения status code 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)

    @testit.title('users autotest for ann')
    @testit.description('Автотесты сущности пользователь')
    @testit.displayName('Автотест для пользователей')
    @testit.externalID('all_autotest_users')
    def test_users_all_testit(self):
        with testit.step('test_check_post_user_create_serializer_data'):
            self.test_check_post_user_create_serializer_data()
        with testit.step('test_profile_user_data'):
            self.test_profile_user_data()
        with testit.step('test_post_login_user'):
            self.test_post_login_user()
        with testit.step('test_delete_user'):
            self.test_delete_user()
        with testit.step('test_change_password'):
            self.test_change_password()