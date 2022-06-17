# https://www.django-rest-framework.org/api-guide/serializers/
import pytest

from goals.serializers import GoalCategorySerializer
from myappcalendar.settings import REST_FRAMEWORK
from tests.factories import UserFactory, GoalCategoryFactory

# REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = None
# REST_FRAMEWORK['PAGE_SIZE'] = None
page_size = REST_FRAMEWORK['PAGE_SIZE']

@pytest.mark.django_db()
def test_create_category_goals(client):
    # Get or create user by username
    testuser = UserFactory(
        username="test1@example.com"
    )
    # Create GoalCategory with username=test1@example.com
    # Remember about page_size
    goalcategory = GoalCategoryFactory.create_batch(page_size, user=testuser)
    # login
    client.force_login(user=testuser)
    response = client.get("/goals/goal_category/list/", content_type='application/json')
    serializer = GoalCategorySerializer(goalcategory, many=True)  # Object -> OrderedDict (сериализация)

    # data = [{
    #     'id': '1',
    #     'title': 'test'
    # }, ]
    # Больше нужно для проверки POST.
    # serializer = GoalCategorySerializer(data=data, many=True)  # json -> OrderedDict(десериализация)
    # serializer.is_valid(raise_exception=True)
    # print(serializer.validated_data)
    assert response.data["results"] == serializer.data
