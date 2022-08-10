# https://www.django-rest-framework.org/api-guide/serializers/
import os
import pprint
import testit
import pytest
from freezegun import freeze_time
from django.test import TestCase
from goals.models import GoalCategory, Board, Goal, BoardParticipant, GoalComment
from goals.serializers import GoalCategoryListSerializer, BoardListSerializer, BoardSerializer, GoalListSerializer, \
    GoalRUDASerializer, GoalCommentListSerializer
from tests.factories import UserFactory, GoalCategoryFactory, BoardParticipantFactory, BoardFactory, GoalFactory, \
    GoalCommentsFactory
from rest_framework.test import APIClient
from faker import Faker

# TODO не смог использовать fixtures в TestCase
from users.models import User


class Test_goal(TestCase):
    # В данном тесткейсе не делаем акцент на захешированный пароль в отлиичии от testusers
    def setUp(self):
        self.faker = Faker()
        self.testuser = UserFactory(
            username="test1@example.com",
        )
        self.client = APIClient()  # APIClient(enforce_csrf_checks=True)


    """
    Test Goals Category
    """

    # hidden field не даст диссериализовать Json→ dict
    def test_create_category_goals(self):
        # Create GoalCategory with username=test1@example.com
        # ------ Remember about page_size not actual ------
        """
            В случае если будет указан self.testuser, другой нужно будет создать Board с таким же пользователем.
            board = BoardFactory.create(user=self.testuser2)
        """
        # login
        self.client.force_login(user=self.testuser)
        goalcategory = GoalCategoryFactory.create_batch(size=1, user=self.testuser)
        response = self.client.get("/goals/goal_category/list/", content_type='application/json')
        serializer = GoalCategoryListSerializer(goalcategory, many=True)  # Object -> OrderedDict (сериализация)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)  # assert response.data["results"]
        #Добавляем выход пользователя.
        self.client.logout()

    def test_not_authorized_list_goal_categories(self):
        """
        В случае если будет указан self.testuser, другой нужно будет создать Board с таким же пользователем.
        board = BoardFactory.create(user=self.testuser2)
        """
        goalcategory = GoalCategoryFactory.create(user=self.testuser)
        response = self.client.get(f"/goals/goal_category/{goalcategory.pk}/", content_type='application/json')
        pprint.pprint(response.json())
        assert response.status_code == 403

    def test_retrieve_goal_categories(self):
        self.client.force_login(user=self.testuser)
        goalcategory = GoalCategoryFactory.create(user=self.testuser)
        response = self.client.get(f"/goals/goal_category/{goalcategory.pk}/", content_type='application/json')
        serializer = GoalCategoryListSerializer(goalcategory, many=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)  # Object -> OrderedDict (сериализация)
        self.client.logout()

    def test_delete_goal_category(self):
        self.client.force_login(user=self.testuser)
        goalcategory = GoalCategoryFactory.create(user=self.testuser)
        response = self.client.delete(f"/goals/goal_category/{goalcategory.pk}/", content_type='application/json')
        # TODO Можно проверить на наличие в БД
        self.assertEqual(response.status_code, 204)
        self.client.logout()

    @freeze_time("2020-07-07 00:00:00", tz_offset=-3)
    def test_post_category_goal(self):
        board = BoardFactory.create()
        data = {
            "title": "string",
            "board": board.id
        }
        self.client.force_login(user=self.testuser)
        response = self.client.post("/goals/goal_category/create/", data=data)
        expected_response = {
            "id": GoalCategory.objects.last().pk,
            "title": "string",
            "is_deleted": False,
            "created": '2020-07-07T00:00:00+03:00',
            "updated": '2020-07-07T00:00:00+03:00',
            "board": board.id
        }
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, 201)
        self.client.logout()

    def test_not_participant_post_category_goal(self):
        board = BoardFactory.create()
        data = {
            "title": "string",
            "board": board.id
        }
        testuser2 = UserFactory(
            username="test2@example.com"
        )
        self.client.force_login(user=testuser2)
        response = self.client.post("/goals/goal_category/create/", data=data)
        assert response.status_code == 403
        self.client.logout()

    """
        Test boards
    """

    def test_boardlist(self):
        # Create boardlist with username=test1@example.com
        # ------ Remember about page_size not actual ------
        # login
        self.client.force_login(user=self.testuser)
        boards = BoardFactory.create_batch(size=5, user=self.testuser)
        response = self.client.get("/goals/board/list/", content_type='application/json')
        serializer = BoardListSerializer(boards, many=True)  # Object -> OrderedDict (сериализация)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)  # assert response.data["results"]

    def test_retrieve_board(self):
        # Create board with username=test1@example.com
        # ------ Remember about page_size not actual ------
        # login
        self.client.force_login(user=self.testuser)
        boards = BoardFactory.create()
        response = self.client.get(f"/goals/board/{boards.pk}/", content_type='application/json')
        serializer = BoardSerializer(boards, many=False)  # Object -> OrderedDict (сериализация)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)  # assert response.data["results"]

    @freeze_time("2020-07-07 00:00:00", tz_offset=-3)
    def test_post_create_board(self):
        title = self.faker.name()
        data = {
            "title": title,
            "is_deleted": False
        }
        self.client.force_login(user=self.testuser)
        response = self.client.post("/goals/board/create/", data=data)

        expected_response = {
            "id": Board.objects.last().pk,
            "created": '2020-07-07T00:00:00+03:00',
            "updated": '2020-07-07T00:00:00+03:00',
            "title": title,
            "is_deleted": False
        }
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, 201)

    def test_delete_board(self):
        self.client.force_login(user=self.testuser)
        board = BoardFactory.create()
        response = self.client.delete(f"/goals/board/{board.pk}/", content_type='application/json')
        # TODO Можно проверить на наличие в БД
        self.assertEqual(response.status_code, 204)

    def test_delete_not_another_user_board(self):
        testuser2 = UserFactory(
            username="test2@example.com"
        )
        self.client.force_login(user=testuser2)
        board = BoardFactory.create()
        response = self.client.delete(f"/goals/board/{board.pk}/", content_type='application/json')
        # TODO Можно проверить на наличие в БД
        # Так как для пользователя будет страница не найдена.
        self.assertEqual(response.status_code, 404)

    def test_delete_not_owner_board(self):
        testuser2 = UserFactory(
            username="test2@example.com"
        )
        self.client.force_login(user=testuser2)
        board = BoardFactory.create()
        # Создаю участника доски но с другими правами.
        boardparticipant = BoardParticipantFactory(user=testuser2, board=board, role=3)
        response = self.client.delete(f"/goals/board/{board.pk}/", content_type='application/json')
        # TODO Можно проверить на наличие в БД
        self.assertEqual(response.json()['detail'], "У вас недостаточно прав для выполнения данного действия.")
        self.assertEqual(response.status_code, 403)

    """
        Test Goals
    """

    def test_list_goals(self):
        # login
        self.client.force_login(user=self.testuser)
        # Пользователя указываем всегда так как создается в Factory несколько пользователей.
        goals = GoalFactory.create_batch(size=1, user=self.testuser)
        response = self.client.get("/goals/goal/list/", content_type='application/json')
        serializer = GoalListSerializer(goals, many=True)  # Object -> OrderedDict (сериализация)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)  # assert response.data["results"]

    def test_retrieve_goal(self):
        # login
        self.client.force_login(user=self.testuser)
        # Пользователя указываем всегда так как создается в Factory несколько пользователей.
        goals = GoalFactory.create(user=self.testuser)
        response = self.client.get(f"/goals/goal/{goals.pk}/", content_type='application/json')
        serializer = GoalRUDASerializer(goals, many=False)  # Object -> OrderedDict (сериализация)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    @freeze_time("2020-07-07 00:00:00", tz_offset=-3)
    def test_post_create_goal(self):
        self.client.force_login(user=self.testuser)
        title = self.faker.name()
        description = self.faker.text()
        # Board создается как связанная фабрика с правами на нее от testuser по умолчанию
        goalcategory = GoalCategoryFactory.create(user=self.testuser)
        """
            если есть желание от другого пользователя, то выглядит примерно так.
            board = BoardFactory.create(user=testuser2)
            goalcategory = GoalCategoryFactory.create(user=testuser2, board=board)
        """
        data = {
            "title": title,
            "due_date": "2022-07-07",
            "description": description,
            "status": 1,
            "priority": 1,
            "category": goalcategory.id
        }
        self.client.force_login(user=self.testuser)
        response = self.client.post("/goals/goal/create/", data=data)
        expected_response = {
            "id": Goal.objects.last().pk,
            "due_date": "2022-07-07",
            "created": '2020-07-07T00:00:00+03:00',
            "updated": '2020-07-07T00:00:00+03:00',
            "title": title,
            "description": description,
            "status": 1,
            "priority": 1,
            "category": goalcategory.id
        }
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, 201)

    def test_delete_goal(self):
        self.client.force_login(user=self.testuser)
        # Пользователя указываем всегда так как создается в Factory несколько пользователей.
        goal = GoalFactory.create(user=self.testuser)
        response = self.client.delete(f"/goals/goal/{goal.pk}/", content_type='application/json')
        # # TODO Можно проверить на наличие в БД
        self.assertEqual(response.status_code, 204)

    """
            Test GoalComment
    """

    def test_list_goalcomment(self):
        # login
        self.client.force_login(user=self.testuser)
        goal_comment = GoalCommentsFactory.create_batch(size=1, user=self.testuser)
        response = self.client.get("/goals/goal_comment/list/", content_type='application/json')
        serializer = GoalCommentListSerializer(goal_comment, many=True)  # Object -> OrderedDict (сериализация)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)  # assert response.data["results"]

    def test_retrieve_goalcomment(self):
        # login
        self.client.force_login(user=self.testuser)
        # Пользователя указываем всегда так как создается в Factory несколько пользователей.
        goal_comment = GoalCommentsFactory.create(user=self.testuser)
        response = self.client.get(f"/goals/goal_comment/{goal_comment.pk}/", content_type='application/json')
        serializer = GoalCommentListSerializer(goal_comment, many=False)  # Object -> OrderedDict (сериализация)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_goalcomment_not_participant(self):
        testuser2 = UserFactory(
            username="test2@example.com"
        )
        self.client.force_login(user=testuser2)
        # Пользователя указываем всегда так как создается в Factory несколько пользователей.
        goal_comment = GoalCommentsFactory.create(user=self.testuser)
        response = self.client.get(f"/goals/goal_comment/{goal_comment.pk}/", content_type='application/json')
        serializer = GoalCommentListSerializer(goal_comment, many=False)  # Object -> OrderedDict (сериализация)
        # В данном случае not found так как он не участником доски
        self.assertEqual(response.status_code, 404)

    @freeze_time("2020-07-07 00:00:00", tz_offset=-3)
    def test_post_create_goal_comment(self):
        self.client.force_login(user=self.testuser)
        text = self.faker.text()
        # Board создается как связанная фабрика с правами на нее от testuser по умолчанию
        goal = GoalFactory.create(user=self.testuser)
        data = {
            "text": text,
            "goal": goal.id
        }
        response = self.client.post("/goals/goal_comment/create/", data=data)
        expected_response = {
            "id": GoalComment.objects.last().pk,
            "created": '2020-07-07T00:00:00+03:00',
            "updated": '2020-07-07T00:00:00+03:00',
            "text": text,
            "goal": goal.id
        }
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, 201)

    def test_delete_goal_comment(self):
        self.client.force_login(user=self.testuser)
        # Пользователя указываем всегда так как создается в Factory несколько пользователей.
        goal_comment = GoalCommentsFactory.create(user=self.testuser)
        response = self.client.delete(f"/goals/goal_comment/{goal_comment.pk}/", content_type='application/json')
        # # TODO Можно проверить на наличие в БД
        self.assertEqual(response.status_code, 204)

    def test_delete_goalcomment_not_current_user(self):
        testuser2 = UserFactory(
            username="test2@example.com"
        )
        # Пользователь участник доски, но не автор комментария
        self.client.force_login(user=testuser2)
        goal_comment = GoalCommentsFactory.create(user=self.testuser)
        # Наделяем правами пользователя testuser2 на существующую доску
        title = Board.objects.last().title
        # TODO как ивлечь по id или last в Factory не ясно
        board = BoardFactory(user=testuser2, title=title)
        response = self.client.delete(f"/goals/goal_comment/{goal_comment.pk}/", content_type='application/json')
        self.assertEqual(response.status_code, 403)

    @testit.title('категории в целях')
    @testit.description('Автотест для сущности категории цели')
    @testit.displayName('Автотест для категорий')
    @testit.externalID('Goals Category')
    def test_goals_all_testit(self):
        with testit.step('test_create_category_goals'):
            self.test_create_category_goals()
        with testit.step('test_profile_user_data'):
            self.test_not_authorized_list_goal_categories()
        with testit.step('test_retrieve_goal_categories'):
            self.test_retrieve_goal_categories()
        with testit.step('test_delete_goal_category'):
            self.test_delete_goal_category()
        with testit.step('test_post_category_goal'):
            self.test_post_category_goal()
        with testit.step('test_not_participant_post_category_goal'):
            self.test_not_participant_post_category_goal()

# example without testcase
# https://pytest-factoryboy.readthedocs.io/en/stable/#model-fixture
# https://pytest-factoryboy.readthedocs.io/en/stable/#model-fixture
# @pytest.mark.django_db()
# def test_retrieve_goal_categories(client, board):
#     # Get or create user by username
#     testuser = UserFactory(
#         username="test1@example.com"
#     )
#     client.force_login(user=testuser)
#     boardparticipant = BoardParticipantFactory.create_batch(size=1, user=testuser, board=board)
#     goalcategory = GoalCategoryFactory.create(user=testuser, board=board)
#     response = client.get(f"/goals/goal_category/{goalcategory.pk}/", content_type='application/json')
#     serializer = GoalCategoryListSerializer(goalcategory, many=False)
#     self.assertEqual(response.status_code,  200)
#     # without results": []
#     self.assertEqual(response.data, serializer.data)
# print("Users", User.objects.all().values())
# print("BoardParticipant", BoardParticipant.objects.all().values())
# print("Board", Board.objects.all().values())
# print("GoalCategory", GoalCategory.objects.all().values())
# print("Goal", Goal.objects.all().values())
# print("Goalcomment", GoalComment.objects.all().values())