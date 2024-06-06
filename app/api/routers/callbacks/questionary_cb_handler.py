from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from aiogram.types import CallbackQuery


from aiogram.fsm.context import FSMContext

from api.crud import AsyncOrm

from api.markups import (
    ProfileActions,
    ProfileCbData,
    build_book_card_kb,
    register_profile,
)
from utils import Form
from utils import choice_items
from utils import LEXICON

image_path = "app/utils/images/books.jpg"

router = Router(name=__name__)


@router.callback_query(
    ProfileCbData.filter(
        F.action == ProfileActions.register,
    )
)
async def register_user_handler(
    call: CallbackQuery,
    state: FSMContext,
):
    await call.answer()
    await call.message.answer(text=LEXICON["/register"])
    await state.set_state(Form.username)
    await call.message.answer(
        text=LEXICON["ask_username"],
        reply_markup=register_profile(call.from_user.username),
    )


@router.message(Form.username)
async def form_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.books)
    await message.answer(
        LEXICON["ask_books"],
        reply_markup=register_profile(
            choice_items(LEXICON["books"]),
        ),
    )


@router.message(Form.books)
async def form_books(message: Message, state: FSMContext):
    books = list(message.text)
    if len(books) > 1:
        await state.update_data(books=message.text.split(", "))
        await state.set_state(Form.genre)
        await message.answer(
            LEXICON["ask_genre"],
            reply_markup=register_profile(
                choice_items(LEXICON["genres"]),
            ),
        )
    else:
        await message.answer(LEXICON["not_list"])


@router.message(Form.genre)
async def form_genre(message: Message, state: FSMContext, session):

    await state.update_data(genre=message.text.split(", "))
    data = await state.get_data()
    await state.clear()
    if not message.from_user.username:
        username = data["username"]
    else:
        username = message.from_user.username

    # await AsyncOrm.update_user(
    #     session=session,
    #     tg_id=message.from_user.id,
    #     username=username,
    #     favourite_genre=data["genre"],
    # )
    await AsyncOrm.update_user(
        session=session,
        tg_id=message.from_user.id,
        books=data["books"],
    )
    await message.answer_photo(
        photo=FSInputFile(path=image_path),
        caption=LEXICON["success"],
        reply_markup=build_book_card_kb(),
    )
