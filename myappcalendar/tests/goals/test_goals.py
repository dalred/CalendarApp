# https://www.django-rest-framework.org/api-guide/serializers/
import pytest
from freezegun import freeze_time
from django.test import TestCase
from goals.models import GoalCategory
from goals.serializers import GoalCategoryListSerializer
from tests.factories import UserFactory, GoalCategoryFactory, BoardParticipantFactory, BoardFactory
from rest_framework.test import APIClient


class TestCategory_goal(TestCase):
    def setUp(self):
        self.testuser = UserFactory(
            username="test1@example.com"
        )
        self.client = APIClient(enforce_csrf_checks=True)
        self.board = BoardFactory.create()
        self.boardparticipant = BoardParticipantFactory(user=self.testuser, board=self.board)

    # hidden field не даст диссериализовать Json→ dict
    def test_create_category_goals(self):
        # Create GoalCategory with username=test1@example.com
        # ------ Remember about page_size not actual ------
        # login
        self.client.force_login(user=self.testuser)
        goalcategory = GoalCategoryFactory.create_batch(size=1, user=self.testuser, board=self.board)
        response = self.client.get("/goals/goal_category/list/", content_type='application/json')
        serializer = GoalCategoryListSerializer(goalcategory, many=True)  # Object -> OrderedDict (сериализация)
        assert response.status_code == 200
        assert response.data == serializer.data  # assert response.data["results"]

    def test_retrieve_goal_categories(self):
        self.client.force_login(user=self.testuser)
        goalcategory = GoalCategoryFactory.create(user=self.testuser, board=self.board)
        print('goalcategory.pk', goalcategory.pk)
        response = self.client.get(f"/goals/goal_category/{goalcategory.pk}/", content_type='application/json')
        serializer = GoalCategoryListSerializer(goalcategory, many=False)
        assert response.status_code == 200
        assert response.data == serializer.data  # Object -> OrderedDict (сериализация)


@pytest.mark.django_db
@freeze_time("2020-07-07 00:00:00", tz_offset=-3)
def test_post_category_goal(self, client, board):
    print(self.top)
    data = {
        "title": "string",
        "is_deleted": False,
        "board": 1
    }
    # Check PostData from Any
    testuser = UserFactory(
        username="test1@example.com"
    )
    client.force_login(user=testuser)
    boardparticipant = BoardParticipantFactory.create_batch(size=1, user=testuser, board=board)
    response = client.post("/goals/goal_category/create/", data=data, content_type='application/json')
    expected_response = {
        "id": GoalCategory.objects.last().pk,
        "title": "string",
        "is_deleted": False,
        "created": '2020-07-07T00:00:00+03:00',
        "updated": '2020-07-07T00:00:00+03:00',
        "board": board.pk
    }
    assert response.json() == expected_response
    assert response.status_code == 201
