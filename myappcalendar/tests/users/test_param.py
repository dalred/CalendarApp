import pytest
import testit

@testit.workItemID(18)
@testit.title('Тест параметризованный one')
@testit.description('Автотесты сущности пользователь')
@testit.displayName('Автотест параметризованный one')
@testit.externalID('Тестовый параметризованный тест')
@pytest.mark.parametrize("login, password, expected_login_password", [("testit@testit.ru", "123", "testit@testit.ru_123"), ("testit@testit.ru", "124", "testit@testit.ru_124")])
def test_param_testit(login, password, expected_login_password):
    with testit.step('Первый шаг'):
        assert str(f"{login}_{password}") == expected_login_password


@testit.title('Тест параметризованный')
@testit.description('Автотесты сущности пользователь')
@testit.displayName('Автотест параметризованный')
@testit.externalID('Тестовый параметризованный тест2')
@pytest.mark.parametrize("login, password, expected_login_password", [("testit@testit.ru", "123", "testit@testit.ru_123")])
def test_param2_testit(login, password, expected_login_password):
    with testit.step('Первый шаг'):
        assert str(f"{login}_{password}") == expected_login_password

@testit.title('Тест параметризованный')
@testit.description('Автотесты сущности пользователь')
@testit.displayName('Автотест параметризованный')
@testit.externalID('Тестовый параметризованный тест3')
@pytest.mark.xfail(reason="bug in a 3rd party library")
@pytest.mark.parametrize("login, password, expected_login_password", [("testit@testit.ru", "123", "testit@testit.ru_123")])
def test_param3_testit(login, password, expected_login_password):
    with testit.step('Первый шаг'):
        assert str(f"{login}_{password}") == expected_login_password