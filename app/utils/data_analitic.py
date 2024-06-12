from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from core import User

from api.crud import AsyncOrm
from utils import ai_helper


async def get_favorite_book(session: AsyncSession, user_id) -> str:
    user_book_details = await AsyncOrm.select_user_read_books(
        session=session,
        user_id=user_id,
    )
    best_rating = 0
    favourite_book = None
    for user_book_detail in user_book_details:
        if user_book_detail.rating > best_rating:
            best_rating = user_book_detail.rating
            favourite_book = f"{user_book_detail.book.author}, {user_book_detail.book.title}"
    return favourite_book


def parse_book_info(text: str) -> str:
    left_index = text.index('"') + 1
    right_index = text.rindex('"')
    title = text[left_index:right_index]
    return title


def make_book_data_easy_to_record(books: list) -> dict:
    book_info = {}
    token = ai_helper.create_token()
    for book in books:
        book_info["title"] = book
        prompt = (
            f"Имя и фамилия автора {book}."
            f"Ответ должен быть простой: Имя и фамилия автора, без ковычек и пояснений"
        )

        book_author = ai_helper.send_prompt(token=token, message=prompt)
        book_info["author"] = book_author
    return book_info
