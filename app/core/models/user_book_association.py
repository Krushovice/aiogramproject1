from typing import TYPE_CHECKING, Literal

from sqlalchemy import Float, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .book import Book

Status = Literal["to_read", "read"]


class BookStatus(Enum):
    TO_READ: str = "to_read"
    READ: str = "read"


class UserBookAssociation(Base):
    __tablename__ = "user_book_association"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "book_id",
            name="idx_unique_user_book",
        ),
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey(
            "books.id",
            ondelete="CASCADE",
        )
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    rating: Mapped[float] = mapped_column(
        Float,
        default=0,
        server_default="0",
    )
    status: Mapped[Status]

    book: Mapped["Book"] = relationship(
        back_populates="users_details",
    )
    user: Mapped["User"] = relationship(
        back_populates="books_details",
    )
