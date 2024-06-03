import datetime
from typing import Annotated, TYPE_CHECKING, List

from sqlalchemy import Text, String, Float, ForeignKey, text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

from .association_tables import user_books_table, user_wishlist_table

if TYPE_CHECKING:
    from .user import User


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(150), nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)

    # Читатели книги с их рейтингами

    readers: Mapped[List["User"]] = relationship(
        secondary=user_books_table,
        back_populates="users",
        lazy="selectin",
    )
    wishers: Mapped[List["User"]] = relationship(
        secondary=user_wishlist_table,
        back_populates="users",
        lazy="selectin",
    )

    def __str__(self):
        return f"Book(title={self.title!r}, author={self.author!r})"

    def __repr__(self):
        return str(self)


class Rating(Base):
    __tablename__ = "book_ratings"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
    )
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    read_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=datetime.datetime.now(datetime.UTC),
    )
    user: Mapped["User"] = relationship(
        back_populates="books",
        lazy="selectin",
    )
    book: Mapped["Book"] = relationship(
        back_populates="readers",
        lazy="selectin",
    )

    def __str__(self):

        return f"Rating(book={self.book.title!r}, value={self.rating!r})"

    def __repr__(self):
        return str(self)
