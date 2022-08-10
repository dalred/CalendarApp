import pytest
import testit

@testit.title('Тест параметризованный')
@testit.description('Автотесты сущности пользователь')
@testit.displayName('Автотест параметризованный')
@testit.externalID('Тестовый параметризованный тест')
@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("2+3", 4)])
def test_param_testit(test_input, expected):
    with testit.step('Первый шаг'):
        assert eval(test_input) == expected
