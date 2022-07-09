import pytest

@pytest.mark.django_db()
def test_one(tgclient):
    print(tgclient)