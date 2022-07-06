import random
from django.utils import timezone
import factory.fuzzy
from datetime import datetime as dt

from goals.models import GoalCategory, Board, BoardParticipant
from users.models import User


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Sequence(lambda n: f'TestBoard{n + 1}')
    is_deleted = False


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f'test{n + 1}@example.com')
    password = 'password'


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
    # updated = factory.Faker('iso8601', tzinfo=timezone.get_current_timezone())
