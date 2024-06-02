from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from typing import Sequence

from core.models import User, Book, Author


class AsyncOrm:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self,
        tg_id: int,
        username: str,
        full_name: str,
    ) -> None:

        user = User(
            tg_id=tg_id,
            username=username,
            full_name=full_name,
        )
        self.session.add(user)
        await self.session.commit()

    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        u = aliased(User)

        query = select(u.full_name).select_from(u).filter(u.tg_id == tg_id)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        res = await self.session.scalar(query)
        if res:
            result = res.one()
            return result
        return None

    # @staticmethod
    # async def select_reader_by_username(username):
    #     r = aliased(Reader)
    #     async with async_session_factory() as session:
    #         query = select(r.id).select_from(r).filter(r.username == username)
    #         print(query.compile(compile_kwargs={"literal_binds": True}))
    #         res = await session.execute(query)
    #         print(res)
    #         if res:
    #             result = res.one()
    #             return result[0]
    #         return None
    #
    # @staticmethod
    # async def select_readers_by_selectin():
    #     async with async_session_factory() as session:
    #         query = select(Reader).options(selectinload(Reader.books))
    #         print(query.compile(compile_kwargs={"literal_binds": True}))
    #         res = await session.execute(query)
    #         if res:
    #             result = res.unique().scalars().all()
    #             return result
    #         return None
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
    # @staticmethod
    # async def insert_book(reader_id: int, book_info: object):
    #     async with async_session_factory() as session:
    #         book = Book(
    #             name=book_info.title,
    #             author=book_info.author,
    #             description=book_info.description,
    #             genre=book_info.categories,
    #             reader_id=reader_id,
    #         )
    #         session.add(book)
    #         await session.commit()
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
    # @staticmethod
    # async def select_books(user_id: int):
    #     # Задаем удонобное имя переменной для работы с ORM
    #     b = aliased(Book)
    #     async with async_session_factory() as session:
    #         query = (
    #             select(b.name)
    #             .select_from(b)
    #             .filter(
    #                 b.reader_id == user_id,
    #             )
    #         )
    #         print(query.compile(compile_kwargs={"literal_binds": True}))
    #         res = await session.execute(query)
    #         result = res.all()
    #         # Извлечение имен книг из результатов запроса
    #         book_names = [book.name for book in result]
    #         print(book_names)
    #         return book_names
