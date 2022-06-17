import json
from typing import Dict

import pytest


@pytest.fixture()
@pytest.mark.django_db
def csrf_admin(client, django_user_model) -> Dict:
    email = "username@username.ru"
    password = "password"

    django_user_model.objects.create_user(
        username=email, password=password, role="admin")

    response = client.post("/core/login/",
                           data={"username": email, "password": password},
                           content_type='application/json'
                           )
    # response.cookies['csrftoken'].value
    return response.json()


@pytest.fixture()
@pytest.mark.django_db
def csrf_user(client, django_user_model) -> Dict:
    email = "test1@username.ru"
    password = "password"

    django_user_model.objects.create_user(
        username=email, password=password, role="user")

    response = client.post("/core/login/",
                           data={"username": email, "password": password},
                           content_type='application/json'
                           )
    # response.cookies['csrftoken'].value
    return response.json()
