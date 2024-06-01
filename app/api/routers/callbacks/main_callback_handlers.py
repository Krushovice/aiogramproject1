from aiogram import Router, F
from aiogram.types import CallbackQuery


from api.markups import (
    MenuCbData,
    MenuActions,
    build_main_kb,
)

from utils import LEXICON


router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.profile))
async def handle_account_button(call: CallbackQuery):
    await call.answer()
