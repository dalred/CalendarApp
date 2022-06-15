import factory.fuzzy
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n + 1}@example.com')
    password = 'password'
