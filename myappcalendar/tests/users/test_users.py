import pytest

from myappcalendar.settings import REST_FRAMEWORK
from tests.factories import UserFactory
from users.serializers import UserListSerializer, UserCreateSerializer
from users.models import User

REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = None


@pytest.mark.django_db
def test_list_token_admin_users(client, jwt_admin_token):
    user = UserFactory.create_batch(5)
    # Не совпадаем по кол-ву пользователей поэтому запрос в базу.
    queryset = User.objects.all()
    response = client.get(f"/api/users/", content_type='application/json',
                          HTTP_AUTHORIZATION="Bearer " + jwt_admin_token)
    print(response.json())
    assert response.status_code == 200
    # (Серилизация  Object → Json)
    assert response.data == UserListSerializer(queryset, many=True).data


@pytest.mark.django_db
def test_list_token_user_users(client, jwt_user_token):
    user = UserFactory.create_batch(5)
    # Не совпадаем по кол-ву пользователей поэтому запрос в базу.
    response = client.get(f"/api/users/", content_type='application/json',
                          HTTP_AUTHORIZATION="Bearer " + jwt_user_token)
    assert response.status_code == 403, "Код ошибки должен быть 403 forbidden"


@pytest.mark.django_db
def test_check_post_data():
    data = {
        "email": "test@test.ru",
        "password": "test"
    }
    # Check PostData from Any
    serializer = UserCreateSerializer(data=data)  # (Десерилизация Json→ dict)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_post(client, user):
    # user creates a record in the database
    data = {
        "password": "test",
        "email": "test@test.ru"
    }
    # Id +1 user+client.post() two records
    expected_data = {
        "id": user.id + 1,
        "email": "test@test.ru",
        "first_name": "Unknown",
        "last_name": "Unknown"
    }
    # We can use client.get() but we want to check client.post
    response = client.post("/api/users/create/", data=data, content_type='application/json')
    assert response.status_code == 201
    # Check PostData from expected_data and expected_response
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_user(client):
    user = UserFactory.create()
    response = client.get(f"/api/users/{user.pk}/")
    assert response.status_code == 200
    assert response.data == UserListSerializer(user).data
