import pytest
import testit


@testit.title('Тест параметризованный')
@testit.description('Автотесты сущности пользователь')
@testit.displayName('Автотест параметризованный')
@testit.externalID('Тестовый параметризованный тест')
@pytest.mark.parametrize("login, password, expected", [("dalred@mail.ru", "123", "dalred@mail.ru_123")])
def test_param_testit(login, password, expected):
    with testit.step('Первый шаг'):
        assert str(f"{login}_{password}") == expected
