from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.types import Message, FSInputFile
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import AsyncOrm
from api.markups import build_main_kb

from utils import LEXICON

router = Router()

image_path = "app/utils/images/books.jpg"


@router.message(CommandStart())
async def command_start_handler(
    message: Message,
    session: AsyncSession,
):

    tg_id = message.from_user.id
    user = await AsyncOrm.get_user_by_tg_id(
        tg_id=tg_id,
        session=session,
    )

    if not user:
        await AsyncOrm.create_user(
            session=session,
            tg_id=tg_id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
        )

    await message.answer_photo(
        photo=FSInputFile(path=image_path),
        caption=LEXICON["/start"],
        reply_markup=build_main_kb(),
    )


@router.message(Command("help"))
async def command_help_handler(message: Message):
    await message.answer_photo(
        photo=FSInputFile(path=image_path),
        caption=LEXICON["/help"],
        reply_markup=build_main_kb(),
    )
