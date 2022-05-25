from pytest_factoryboy import register

pytest_plugins = ['tests.fixtures']

from tests.factories import UserFactory

# Model fixture implements an instance of a model created by the factory.
# Name convention is model’s lowercase-underscore class name.

register(UserFactory)
