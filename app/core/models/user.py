from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import BigInteger, String
from typing import TYPE_CHECKING, List

from .base import Base
from .association_tables import user_wishlist_table, user_books_table

if TYPE_CHECKING:
    from .book import Book, Rating


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        default=str(tg_id),
    )

    # Прочитанные книги с рейтингами
    books: Mapped[List["Book"]] = relationship(
        secondary=user_books_table,
        back_populates="user",
        lazy="selectin",
    )
    wish_list: Mapped[List["Book"]] = relationship(
        secondary=user_wishlist_table,
        back_populates="wishers",
        lazy="selectin",
    )

    def __str__(self):
        return f"User(id={self.id!r}, full_name={self.full_name!r})"

    def __repr__(self) -> str:
        return str(self)
