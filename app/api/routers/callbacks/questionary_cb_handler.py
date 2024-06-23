from aiogram.types import Message, FSInputFile
from aiogram import Router, F, types
from aiogram.types import CallbackQuery


from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import AsyncOrm

from api.markups import (
    ProfileActions,
    ProfileCbData,
    build_book_card_kb,
    register_profile,
    yes_no_kb,
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
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(Form.username)
async def form_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.genre)
    await message.answer(
        LEXICON["ask_genre"],
        reply_markup=register_profile(
            choice_items(LEXICON["genres"]),
        ),
    )


@router.message(Form.genre)
async def form_genre(message: Message, state: FSMContext):

    await state.update_data(genre=message.text)
    await state.set_state(Form.books)
    await message.answer(
        LEXICON["ask_book"],
        reply_markup=types.ReplyKeyboardRemove(),
    ),


@router.message(Form.books)
async def form_books(
    message: Message,
    state: FSMContext,
):
    book_info = message.text.split(",")
    if len(book_info) > 1:
        book = {
            "author": book_info[0],
            "title": book_info[1],
        }
        data = await state.get_data()
        if not data.get("books", None):
            await state.update_data(books=[book])
        else:
            books = data["books"]
            books.append(book)
            await state.update_data(books=books)

        await state.set_state(Form.survey)
        await message.answer(
            text="Добавим еще одну книгу?",
            reply_markup=yes_no_kb(),
        ),
    else:
        await message.answer(
            text="Не понимаю вас😢.Укажите пожалуйста автора книги и название через запятую",
            reply_markup=types.ReplyKeyboardRemove(),
        ),


@router.message(Form.survey, F.text == "Да")
async def handle_add_books_yes(
    message: Message,
    state: FSMContext,
):
    await state.set_state(Form.books)
    text = (
        "Отлично! Давай добавим еще одну книгу в список."
        "Отправьте автора и название через запятую"
    )
    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardRemove(),
    ),


@router.message(Form.survey, F.text == "Нет")
async def handle_add_books_no(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):

    data = await state.get_data()
    await state.clear()
    if not message.from_user.username:
        username = data["username"]
    else:
        username = message.from_user.username
    books = data["books"]

    await AsyncOrm.add_read_books_to_user(
        session=session,
        tg_id=message.from_user.id,
        books=books,
    )

    await AsyncOrm.update_user(
        session=session,
        tg_id=message.from_user.id,
        username=username,
        favourite_genre=data["genre"],
    )
    survey_results = (
        "Ваш профиль успешно создан!🤩\n\n"
        f"Имя пользователя: {markdown.hbold(data["username"])}\n"
        f"Любимый жанр: {markdown.hbold(data["genre"])}\n"
        f"Любимые книги: {markdown.hbold(", ".join(book['title'] for book in books))}"
    )
    # await message.answer(
    #     text=survey_results,
    #     reply_markup=types.ReplyKeyboardRemove(),
    # )

    await message.answer_photo(
        photo=FSInputFile(path=image_path),
        caption=survey_results,
        reply_markup=build_book_card_kb(),
    )


@router.message(Form.survey)
async def handle_survey_could_not_understand(
    message: Message,
):
    await message.answer(
        text=(
            "Не понимаю тебя( "
            f"Пожалуйста, отправь {markdown.hcode('Да')} или {markdown.hcode('Нет')}"
        ),
        reply_markup=yes_no_kb(),
    )
