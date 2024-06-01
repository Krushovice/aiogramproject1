from typing import Any

from sqlalchemy import Integer, and_, or_, select, insert, text
from sqlalchemy.engine import Result
from sqlalchemy.orm import aliased, selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Book, Author, Base, db_helper
from .book_shemas import BookCreate, BookUpdatePartial
from .user_shemas import UserCreate, UserUpdatePartial
from .author_shemas import AuthorCreate, AuthorUpdatePartial


class AsyncOrm:
@staticmethod
async def create_user(
        tg_id: int,
        username: str,
        first_name: str,
        last_name: str,
        books: list | None) -> None:
    async with async_session_factory() as session:
        user = User(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            books=books,
        )
        session.add(user)
        await session.commit()

@staticmethod
async def select_reader_by_id(user_id: int, **kwargs):
    r = aliased(Reader)

    async with async_session_factory() as session:
        query = (
            select(r.first_name, r.last_name)
            .select_from(r)
            .filter(r.reader_id == user_id)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        res = await session.execute(query)
        if res:
            result = res.one()
            return result[0]
        return None

@staticmethod
async def select_reader_by_username(username):
    r = aliased(Reader)
    async with async_session_factory() as session:
        query = select(r.id).select_from(r).filter(r.username == username)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        res = await session.execute(query)
        print(res)
        if res:
            result = res.one()
            return result[0]
        return None

@staticmethod
async def select_readers_by_selectin():
    async with async_session_factory() as session:
        query = select(Reader).options(selectinload(Reader.books))
        print(query.compile(compile_kwargs={"literal_binds": True}))
        res = await session.execute(query)
        if res:
            result = res.unique().scalars().all()
            return result
        return None

@staticmethod
async def update_reader(reader_id: int, **kwargs):
    async with async_session_factory() as session:
        reader = await session.get(Reader, reader_id)
        for key, value in kwargs.items():
            setattr(reader, key, value)
        await session.refresh(reader)
        await session.commit()

@staticmethod
async def insert_book(reader_id: int, book_info: object):
    async with async_session_factory() as session:
        book = Book(
            name=book_info.title,
            author=book_info.author,
            description=book_info.description,
            genre=book_info.categories,
            reader_id=reader_id,
        )
        session.add(book)
        await session.commit()

@staticmethod
async def insert_books(reader_id: int, book_list: list):
    async with async_session_factory() as session:
        books = [
            Book(
                name=book["title"],
                reader_id=reader_id,
                author=book["author"],
                category=["genre"],
            )
            for book in book_list
        ]
        session.add_all(books)
        await session.commit()

@staticmethod
async def select_books(user_id: int):
    # Задаем удонобное имя переменной для работы с ORM
    b = aliased(Book)
    async with async_session_factory() as session:
        query = (
            select(b.name)
            .select_from(b)
            .filter(
                b.reader_id == user_id,
            )
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        res = await session.execute(query)
        result = res.all()
        # Извлечение имен книг из результатов запроса
        book_names = [book.name for book in result]
        print(book_names)
        return book_names
