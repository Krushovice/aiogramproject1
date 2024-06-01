from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown
from aiogram.types import Message
from aiogram import Router

from api.markups import build_main_kb
from utils import LEXICON

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    # user_id = await AsyncOrm.select_reader_by_username(
    #     username=message.from_user.username)

    # if not user_id:
    #     await AsyncOrm.insert_reader(first_name=message.from_user.first_name,
    #                                  last_name=message.from_user.last_name,
    #                                  username=message.from_user.username)

    await message.answer(
        text=markdown.hbold(LEXICON["/start"]),
        reply_markup=build_main_kb(),
    )


@router.message(Command("help"))
async def command_help_handler(message: Message):
    await message.answer(text=LEXICON["/help"])
