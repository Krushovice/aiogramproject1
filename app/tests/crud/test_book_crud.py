import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core import Base, db_helper
from app.api.crud.crud import AsyncOrm
from core import Book
from core import UserBookAssociation


@pytest.fixture
async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
def books():
    books = [
        Book(
            title="Червоточина",
            author="Боб",
            genre="Ужасы",
        ),
        Book(
            title="Улыбка",
            author="Мона Лиза",
            genre="Рассказ",
        ),
        Book(
            title="Оно",
            author="Стивен Кинг",
            genre="Триллер",
        ),
        Book(
            title="Красный нос",
            author="Чехов А.П",
            description="О том, как нос соседей копам сдавал.",
            genre="Рассказ",
        ),
    ]

    return books


async def get_user_books(session: AsyncSession, tg_id: int):
    stmt = (
        select(User)
        .options(
            selectinload(User.books_details).joinedload(UserBookAssociation.book),
        )
        .where(User.tg_id == tg_id)
    )
    user = await session.scalar(stmt)
    for user_book_detail in user.books_details:
        print("-", user_book_detail.book.title)
    # return list(books)
    #


async def get_user_book_assoc(session: AsyncSession, tg_id: int):
    stmt = (
        select(User)
        .options(
            selectinload(User.books_details).joinedload(UserBookAssociation.book),
        )
        .where(User.tg_id == tg_id)
    )
    user = await session.scalar(stmt)

    return user.books_details


# async def add_books_to_user(session: AsyncSession):
#     user = await get_user_book_assoc(session=session, tg_id=1234567)
#     # Проверка, существует ли пользователь
#     if user:
#         # Создание ассоциаций и добавление их к пользователю
#
#         user.books_details.append(
#             UserBookAssociation(
#                 book=new_book1,
#                 rating=4,
#                 status="read",
#             )
#         )
#         user.books_details.append(
#             UserBookAssociation(
#                 book=new_book2,
#                 status="to_read",
#             )
#         )
#
#         await session.commit()
#
#         print("Books successfully added to user's list.")
#
#     else:
#         print("User not found.")


@pytest.mark.usefixtures("create_tables")
class TestBooksCRUD:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def test_count_books(self, books):
        for book in books:
            await AsyncOrm.create_book(self.session, book)
