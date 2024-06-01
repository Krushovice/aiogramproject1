from aiogram import Router, F
from aiogram.types import CallbackQuery


from api.markups import (
    MenuCbData,
    MenuActions,
    build_account_kb,
)

from utils import LEXICON


router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.profile))
async def handle_profile_button(call: CallbackQuery):
    await call.answer()
    # Выводим карточку читателя
    text = "Карточка читателя"
    await call.message.edit_caption(
        caption=text,
        reply_markup=build_account_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.advice))
async def handle_advice_button(call: CallbackQuery):
    await call.answer()


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()


@router.callback_query(MenuCbData.filter(F.action == MenuActions.friends))
async def handle_friends_button(call: CallbackQuery):
    await call.answer()
