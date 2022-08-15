import pytest
import testit


@testit.title('Тест параметризованный')
@testit.description('Автотесты сущности пользователь')
@testit.displayName('Автотест параметризованный')
@testit.externalID('Тестовый параметризованный тест')
@pytest.mark.parametrize("login, password, expected_login_password", [("testit@testit.ru", "123", "testit@testit.ru_123"), ("testit2@testit.ru", "123", "testit@testit.ru_123")])
def test_param_testit(login, password, expected_login_password):
    with testit.step('Первый шаг'):
        assert str(f"{login}_{password}") == expected_login_password
