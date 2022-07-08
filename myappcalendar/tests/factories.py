import random
import factory.fuzzy
from faker import Faker
from goals.models import GoalCategory, Board, BoardParticipant, Goal, GoalComment
from users.models import User


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board
        django_get_or_create = ('title',)

    title = factory.Sequence(lambda n: f'TestBoard{n + 1}')
    is_deleted = False

    @factory.post_generation
    def user(self, create, extracted, **kwargs):
        """
        :param extracted: если указан то даем праву переданному пользователю,
        если None, берем по умолчанию. False создаем board без прав.
        :return:
        """
        if extracted:
            boardparticipant = BoardParticipantFactory(user=extracted, board=self, role=1)
        elif extracted is None:
            testuser = UserFactory(
                username="test1@example.com"
            )
            boardparticipant = BoardParticipantFactory(user=testuser, board=self, role=1)
        elif not extracted:
            return self


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f'test{n + 1}@example.com')
    password = 'password'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}')


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = random.choice([1, 2])


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Sequence(lambda n: f'TestCategory{n + 1}')
    user = factory.SubFactory(UserFactory)
    is_deleted = False
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Sequence(lambda n: f'TestGoal{n + 1}')
    user = factory.SubFactory(UserFactory)
    due_date = factory.Faker('date')
    category = factory.SubFactory(GoalCategoryFactory)
    status = random.choice([1, 2])


class GoalCommentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = factory.Sequence(lambda n: f'Cooment №{n + 1}{Faker().text()}')
    # text = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
