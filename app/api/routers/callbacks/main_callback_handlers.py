import requests
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from api.markups import (
    MenuCbData,
    MenuActions,
    build_account_kb,
    build_main_kb,
)

from api.crud import AsyncOrm
from utils import LEXICON, ai_helper, get_favorite_book

router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.profile))
async def handle_profile_button(call: CallbackQuery, session: AsyncSession):
    await call.answer()
    user = await AsyncOrm.get_user(
        session=session,
        tg_id=call.from_user.id,
    )
    favorite_book = await get_favorite_book(session=session, user_id=user.id)
    # Выводим карточку читателя
    text = (
        "<b>Карточка читателя</b> 🪪\n\n"
        f"Никнейм: {user.username if user.username else user.full_name}\n"
        f"Прочитано : 0\n"
        f"Любимый жанр: {user.favorite_genre}\n"
        f"Любимая книга: {favorite_book.title}\n"
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=build_account_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.advice))
async def handle_advice_button(call: CallbackQuery):
    await call.answer()
    message = ""
    try:
        token = ai_helper.create_token()
        res = ai_helper.send_prompt(token=token, message=message)
        await call.message.edit_caption(
            caption=res,
            reply_markup=build_main_kb(),
        )

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при работе с гигачат апи {e}")


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()


@router.callback_query(MenuCbData.filter(F.action == MenuActions.friends))
async def handle_friends_button(call: CallbackQuery):
    await call.answer()
