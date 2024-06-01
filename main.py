import asyncio


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from api.routers import router as main_router
from core.config import settings


async def main() -> None:
    # logger = setup_logger(__name__)
    try:

        dp = Dispatcher()
        bot = Bot(
            token=settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        # Регистриуем роутеры в диспетчере
        dp.include_routers(
            main_router,
        )

        # Пропускаем накопившиеся апдейты и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.session.close()
        # await create_tables()
        # await check_users(bot)

        await dp.start_polling(bot)

    except Exception as e:
        print(f"Ошибка при запуске основного скрипта: {e}")


if __name__ == "__main__":
    asyncio.run(main())
