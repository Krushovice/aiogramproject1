from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import AsyncOrm
from api.markups import (
    ProfileActions,
    ProfileCbData,
    build_book_card_kb,
    build_account_kb,
    build_book_interaction_kb,
)

from utils import LEXICON, ai_helper


router = Router(name=__name__)


@router.callback_query(ProfileCbData.filter(F.action == ProfileActions.read))
async def handle_read_button(
    call: CallbackQuery,
    callback_data: ProfileCbData,
    session: AsyncSession,
):
    await call.answer()
    try:
        prompt = (
            f"Имя и фамилия автора {callback_data.book_title}."
            f"Ответ должен быть простой: Имя и фамилия автора, без ковычек и пояснений"
        )
        token = ai_helper.create_token()
        book_author = ai_helper.send_prompt(token=token, message=prompt)

        await AsyncOrm.add_book_to_read(
            session=session,
            tg_id=call.from_user.id,
            book_title=callback_data.book_title,
            book_author=book_author,
        )
    except Exception as e:
        print(f"При добавлении книги в бд произошла ошибка: {e}")
    await call.message.edit_caption(
        caption="Книга добавлена в ваш список для прочтения!✅😍",
        reply_markup=build_account_kb(is_register=True),
    )
