from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from core import User

from api.crud import AsyncOrm


async def get_favorite_book(session: AsyncSession, user_id) -> str:
    user_book_details = await AsyncOrm.select_user_favorite_book(
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

