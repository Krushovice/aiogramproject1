import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core import Base, db_helper
from app.api.crud.crud import AsyncOrm
from core import User
from core import UserBookAssociation
from utils import get_favourite_book


async def create_tables():
    async with db_helper.engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_user(session: AsyncSession) -> None:
    await AsyncOrm.create_user(
        session=session,
        tg_id=1234567,
        username="Franky",
        full_name="Frank Ocean",
    )


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


async def add_books_to_user(session: AsyncSession):
    user = await get_user_book_assoc(session=session, tg_id=1234567)
    # Проверка, существует ли пользователь
    if user:
        # Создание ассоциаций и добавление их к пользователю

        user.books_details.append(
            UserBookAssociation(
                book=new_book1,
                rating=4,
                status="read",
            )
        )
        user.books_details.append(
            UserBookAssociation(
                book=new_book2,
                status="to_read",
            )
        )

        await session.commit()

        print("Books successfully added to user's list.")

    else:
        print("User not found.")


async def create_books(session: AsyncSession):

    book1 = await AsyncOrm.create_book(
        session=session,
        title="Червоточина",
        author="Боб",
        genre="Ужасы",
    )

    book2 = await AsyncOrm.create_book(
        session=session,
        title="Улыбка",
        author="Мона Лиза",
        genre="Рассказ",
    )

    book3 = await AsyncOrm.create_book(
        session=session,
        title="Оно",
        author="Стивен Кинг",
        genre="Триллер",
    )

    book4 = await AsyncOrm.create_book(
        session=session,
        title="Красный нос",
        author="Чехов А.П",
        description="О том, как нос соседей копам сдавал.",
        genre="Рассказ",
    )

    book5 = await AsyncOrm.create_book(
        session=session,
        title="Червоточина",
        author="Боб",
        genre="Ужасы",
    )

    book6 = await AsyncOrm.create_book(
        session=session,
        title="Улыбка",
        author="Мона Лиза",
        genre="Рассказ",
    )
    return [book1, book2, book3, book4, book5, book6]


async def m2m(session: AsyncSession) -> None:
    user = await create_user(session)


async def main():
    await create_tables()
    async with db_helper.session_factory() as session:
        # await create_books(session=session)
        # await create_user(session)
        # await add_books_to_user(session)
        # user_book_assoc = await AsyncOrm.get_user_books(session, tg_id=1234567)
        # wish_list = await AsyncOrm.select_user_wish_list(session, user_id=1)
        # for book_detail in wish_list:
        #     print("-", book_detail.book.title)

        book = await get_favourite_book(session, 1)
        print(book)


if __name__ == "__main__":
    asyncio.run(main())
