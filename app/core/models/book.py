import datetime
from typing import Annotated, TYPE_CHECKING, List

from sqlalchemy import Text, String, Float, ForeignKey, text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

from .association_tables import user_books_table, user_wishlist_table

if TYPE_CHECKING:
    from .user import User
    from .user_book_association import UserBookAssociation


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(150), nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)

    user_details: Mapped[List["UserBookAssociation"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )
    # users: Mapped[List["User"]] = relationship(
    #     secondary="user_book_association", back_populates="books"
    # )

    def __str__(self):
        return f"Book(title={self.title!r}, author={self.author!r})"

    def __repr__(self):
        return str(self)
