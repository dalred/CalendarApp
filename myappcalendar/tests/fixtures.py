import pytest


@pytest.fixture()
@pytest.mark.django_db
def jwt_admin_token(client, django_user_model):
    email = "admin@username.ru"
    password = "password"

    django_user_model.objects.create_user(
        email=email, password=password, role="admin")

    response = client.post(
        "/api/token/",
        {"email": email, "password": password},
        format='json'
    )
    return response.data["access"]

@pytest.fixture()
@pytest.mark.django_db
def jwt_user_token(client, django_user_model):
    email = "username@username.ru"
    password = "password"

    django_user_model.objects.create_user(
        email=email, password=password, role="user")

    response = client.post(
        "/api/token/",
        {"email": email, "password": password},
        format='json'
    )
    return response.data["access"]