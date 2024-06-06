from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from typing import Sequence

from core.models import User, Book, UserBookAssociation


class AsyncOrm:

    @staticmethod
    async def create_user(
        session: AsyncSession,
        tg_id: int,
        username: str,
        full_name: str,
    ) -> None:

        user = User(
            tg_id=tg_id,
            username=username,
            full_name=full_name,
        )
        session.add(user)
        await session.commit()

    @staticmethod
    async def get_user(session: AsyncSession, tg_id: int) -> User | None:

        stmt = select(User).filter(User.tg_id == tg_id)
        res: Result = await session.execute(stmt)
        user: User = res.scalar_one_or_none()
        return user

    @staticmethod
    async def get_user_books(session: AsyncSession, tg_id: int) -> list[Book]:

        stmt = (
            select(User.book_details)
            .filter(User.tg_id == tg_id)
            .options(
                selectinload(User.book_details).joinedload(UserBookAssociation.book)
            )
        )
        books = await session.scalars(stmt)
        return list(books)

    @staticmethod
    async def create_book(
        session: AsyncSession,
        title: str,
        author: str,
        genre: str | None = None,
        description: str | None = None,
    ):
        book = Book(
            title=title,
            author=author,
            genre=genre,
            description=description,
        )

        session.add(book)
        await session.commit()
        return book

    @staticmethod
    async def update_user(
        session: AsyncSession,
        tg_id: int,
        **kwargs,
    ):

        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)
        for key, value in kwargs.items():
            setattr(user, key, value)
        await session.refresh(user)
        await session.commit()

    @staticmethod
    async def update_user_books(
        session: AsyncSession,
        tg_id: int,
        books: list | None = None,
        wish_list: list | None = None,
    ):
        stmt = (
            select(User)
            .options(
                selectinload(User.books),
            )
            .where(User.tg_id == tg_id)
        )
        user = await session.scalar(stmt)
        if books:
            user.books.append(*books)
        if wish_list:
            user.wish_list.append(*wish_list)

        await session.refresh(user)
        await session.commit()

    @staticmethod
    async def select_user_wish_list(session: AsyncSession, tg_id: int):
        stmt = (
            select(User.wish_list)
            .where(User.tg_id == tg_id)
            .options(selectinload(User.wish_list))
        )
        res: Result = await session.execute(stmt)
        wish_list = res.scalars().all()
        return wish_list

    #
    # @staticmethod
    # async def update_reader(reader_id: int, **kwargs):
    #     async with async_session_factory() as session:
    #         reader = await session.get(Reader, reader_id)
    #         for key, value in kwargs.items():
    #             setattr(reader, key, value)
    #         await session.refresh(reader)
    #         await session.commit()
    #

    #
    # @staticmethod
    # async def insert_books(reader_id: int, book_list: list):
    #     async with async_session_factory() as session:
    #         books = [
    #             Book(
    #                 name=book["title"],
    #                 reader_id=reader_id,
    #                 author=book["author"],
    #                 category=["genre"],
    #             )
    #             for book in book_list
    #         ]
    #         session.add_all(books)
    #         await session.commit()
    #
    @staticmethod
    async def select_books(session: AsyncSession):

        stmt = select(Book).order_by(Book.title)

        res = await session.execute(stmt)
        result = res.scalars().all()

        return result

    @staticmethod
    async def get_average_rating(session, book_id):

        stmt = select(BookRating.rating).filter(BookRating.book_id == book_id)
        res: Result = await session.execute(stmt)
        ratings = res.scalars().all()
        # Вычисляем средний рейтинг
        total_rating = sum(r for r in ratings)
        average_rating = total_rating / len(ratings) if ratings else 0

        return average_rating
