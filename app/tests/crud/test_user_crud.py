import pytest
from app.core import User


@pytest.fixture
def create_user() -> list:
    users = [
        User(
            tg_id=1234567,
            username="Franky",
            full_name="Frank Ocean",
        ),
        User(
            tg_id=12345671232,
            username="Kate",
            full_name="Kaitlyn Clark",
        ),
    ]

    return users


class TestUserCRUD:
    pass
