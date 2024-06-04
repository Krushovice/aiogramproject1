import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Base, User, UserRead, db_helper, settings
from app.api.crud.crud import AsyncOrm


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    # await create_tables()
    # await AsyncOrm.create_user(
    #     session=session,
    #     tg_id=1234567,
    #     username="Franky",
    #     full_name="Frank Ocean",
    # )
    # await AsyncOrm.create_book(
    #     session=session,
    #     title="Червоточина",
    #     author="Боб",
    #     genre="Ужасы",
    # )
    #
    # await AsyncOrm.create_book(
    #     session=session,
    #     title="Улыбка",
    #     author="Мона Лиза",
    #     genre="Рассказ",
    # )
    #
    # await AsyncOrm.create_book(
    #     session=session,
    #     title="Оно",
    #     author="Стивен Кинг",
    #     genre="Триллер",
    # )
    async with db_helper.session_factory() as session:
        # book = await AsyncOrm.create_book(
        #     session=session,
        #     title="Красный нос",
        #     author="Чехов А.П",
        #     description="О том, как нос соседей копам сдавал.",
        #     genre="Рассказ",
        # )
        user = await AsyncOrm.get_user(session=session, tg_id=1234567)

        # books = await AsyncOrm.select_books(session=session)
        # for book in books:
        #     if book.title == "Оно":
        #         await AsyncOrm.update_user(
        #             session=session, tg_id=user.tg_id, books=[book]
        #         )


if __name__ == "__main__":
    asyncio.run(main())
