import factory.fuzzy

from goals.models import GoalCategory
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    username = factory.Sequence(lambda n: f'test{n + 1}@example.com')
    password = 'password'



class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Sequence(lambda n: f'testcategory{n + 1}')
    user = factory.SubFactory(UserFactory)
    is_deleted = False
