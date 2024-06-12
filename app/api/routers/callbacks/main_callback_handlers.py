import requests
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from api.markups import (
    MenuCbData,
    MenuActions,
    build_account_kb,
    build_main_kb,
    build_book_interaction_kb,
)

from api.crud import AsyncOrm
from utils import LEXICON, ai_helper, get_favorite_book, parse_book_info

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
        f"Любимый жанр: {user.favorite_genre if user.favorite_genre else ""}\n"
        f"Любимая книга: {favorite_book.title if favorite_book else ""}\n"
    )
    await call.message.edit_caption(
        caption=text,
        reply_markup=build_account_kb(),
    )


@router.callback_query(MenuCbData.filter(F.action == MenuActions.advice))
async def handle_advice_button(call: CallbackQuery, session: AsyncSession):
    await call.answer()
    user = await AsyncOrm.get_user(
        session=session,
        tg_id=call.from_user.id,
    )
    user_book_assoc = await AsyncOrm.select_user_read_books(
        session=session, user_id=user.id
    )
    books = set()
    for user_book_detail in user_book_assoc:
        books.add(user_book_detail.book.title)
    message = (
        f'Порекомендуй одну книгу, исходя из списка прочитанного{",".join(books)}.'
        "Ответ должен быть интересным, с пояснением."
        'Название книги должно быть без ковычек после слова "рекомендую:".'
        "Предложение должно заканчиваться точкой"
        "Книга не должна присутствовать в books и должна быть схожей по жанру"
    )

    try:
        token = ai_helper.create_token()
        res = ai_helper.send_prompt(token=token, message=message)
        print(res)
        book_title = parse_book_info(res)
        await call.message.edit_caption(
            caption=res,
            reply_markup=build_book_interaction_kb(book_cb_data=book_title),
        )

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при работе с гигачат апи {e}")


@router.callback_query(MenuCbData.filter(F.action == MenuActions.support))
async def handle_support_button(call: CallbackQuery):
    await call.answer()


@router.callback_query(MenuCbData.filter(F.action == MenuActions.friends))
async def handle_friends_button(call: CallbackQuery):
    await call.answer()
