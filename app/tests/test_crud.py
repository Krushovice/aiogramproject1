import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Base, User, UserRead, db_helper, settings
from app.api.crud.crud import AsyncOrm


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main(session: AsyncSession = db_helper.session_getter()) -> User:
    # await create_tables()
    await AsyncOrm.create_user(
        session=session,
        tg_id=1234567,
        username="Franky",
        full_name="Frank Ocean",
    )

    user = await AsyncOrm.get_user_by_tg_id(session=session, tg_id=1234567)

    print(user)
    return user


if __name__ == "__main__":
    asyncio.run(main())
