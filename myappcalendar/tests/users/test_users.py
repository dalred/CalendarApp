import pytest

from myappcalendar.settings import REST_FRAMEWORK
from tests.factories import UserFactory
from users.serializers import UserCreateSerializer, UserCurrentSerializer
#from users.models import User

REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = None


# @pytest.mark.django_db
# def test_list_token_admin_users(client, jwt_admin_token):
#     user = UserFactory.create_batch(5)
#     # Не совпадаем по кол-ву пользователей поэтому запрос в базу.
#     queryset = User.objects.all()
#     response = client.get(f"/core/signup/", content_type='application/json',
#                           HTTP_AUTHORIZATION="Bearer " + jwt_admin_token)
#     print(response.json())
#     assert response.status_code == 200
#     # (Серилизация  Object → Json)
#     assert response.data == UserListSerializer(queryset, many=True).data
#
#
# @pytest.mark.django_db
# def test_list_token_user_users(client, csrf_user_token):
#     user = UserFactory.create_batch(5)
#     # Не совпадаем по кол-ву пользователей поэтому запрос в базу.
#     response = client.get(f"/core/signup/", content_type='application/json',
#                           HTTP_AUTHORIZATION="Bearer " + jwt_user_token)
#     assert response.status_code == 403, "Код ошибки должен быть 403 forbidden"


@pytest.mark.django_db
def test_check_user_create_serializer_data():
    data = {
        "username": "test@test.ru",
        "password": "test",
        "password_repeat": "test",
    }
    # Check PostData from Any
    serializer = UserCreateSerializer(data=data)  # (Десерилизация Json→ dict)
    assert serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_user(client, user):
    # user creates a record in the database
    data = {
        "password": "test",
        "password_repeat": "test",
        "username": "test@test.ru"
    }
    # Id +1 user+csrf_user two records
    expected_data = {
        "id": user.id + 1,
        "username": "test@test.ru",
        "first_name": "Unknown",
        "last_name": "Unknown",
        "email": None
    }
    # We can use client.get() but we want to check client.post
    response = client.post("/core/signup/", data=data, content_type='application/json')
    assert response.status_code == 201
    # Check PostData from expected_data and expected_response
    assert response.data == expected_data

"""
with csrf_user
"""
@pytest.mark.django_db
def test_retrieve_user(client, csrf_user):
    # csrf_user creates a record in the database
    response = client.get("/core/profile/", content_type='application/json')
    assert response.status_code == 200
    # Check PostData from expected_data and expected_response
    user = response.json()
    assert user == UserCurrentSerializer(user).data


@pytest.mark.django_db
def test_delete_user(client, csrf_user):
    # csrf_user creates a record in the database
    response = client.delete("/core/profile/", content_type='application/json')
    assert response.status_code == 204


