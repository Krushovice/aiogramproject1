import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core import Base, User, UserRead, db_helper, settings
from app.api.crud.crud import AsyncOrm
from core import Book
from core.models import UserBookAssociation
from core.models.user_book_association import BookStatus


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_user(session: AsyncSession) -> None:
    await AsyncOrm.create_user(
        session=session,
        tg_id=1234567,
        username="Franky",
        full_name="Frank Ocean",
    )

    user = await AsyncOrm.get_user(session=session, tg_id=1234567)
    return user


async def get_user_books(session: AsyncSession, tg_id: int):
    stmt = (
        select(User)
        .options(
            selectinload(User.book_details).joinedload(UserBookAssociation.book),
        )
        .where(User.tg_id == tg_id)
    )
    user = await session.scalar(stmt)
    for user_book_detail in user.book_details:
        print("-", user_book_detail.book.title)
    # return list(books)
    #


async def add_books_to_user(session: AsyncSession, tg_id: int):
    stmt = (
        select(User)
        .options(
            selectinload(User.book_details).joinedload(UserBookAssociation.book),
        )
        .where(User.tg_id == tg_id)
    )
    user = await session.scalar(stmt)

    # Проверка, существует ли пользователь
    if user:
        new_book1 = Book(title="book1", author="NAME1")
        new_book2 = Book(title="book2", author="NAME2")
        # Создание ассоциаций и добавление их к пользователю
        user.book_details.append(
            UserBookAssociation(
                book=new_book1,
                rating=4.0,
                status=BookStatus.READ,
            )
        )
        user.book_details.append(
            UserBookAssociation(
                book=new_book2,
                status=BookStatus.TO_READ,
            )
        )

        # Добавление новых книг в сессию
        session.add(new_book1)
        session.add(new_book2)
        await session.refresh(user)
        # Сохранение изменений
        await session.commit()

        print("Books successfully added to user's list.")

    else:
        print("User not found.")


async def create_books(session: AsyncSession) -> None:

    await AsyncOrm.create_book(
        session=session,
        title="Червоточина",
        author="Боб",
        genre="Ужасы",
    )

    await AsyncOrm.create_book(
        session=session,
        title="Улыбка",
        author="Мона Лиза",
        genre="Рассказ",
    )

    await AsyncOrm.create_book(
        session=session,
        title="Оно",
        author="Стивен Кинг",
        genre="Триллер",
    )

    book = await AsyncOrm.create_book(
        session=session,
        title="Красный нос",
        author="Чехов А.П",
        description="О том, как нос соседей копам сдавал.",
        genre="Рассказ",
    )


async def m2m(session: AsyncSession) -> None:
    user = await create_user(session)


async def main():
    await create_tables()
    async with db_helper.session_factory() as session:
        await create_books(session=session)
        # await create_user(session)
        # await add_books_to_user(session, tg_id=1234567)


if __name__ == "__main__":
    asyncio.run(main())
