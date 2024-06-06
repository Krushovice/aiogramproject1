from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .book import Book


class BookStatus(Enum):
    TO_READ = "to_read"
    READ = "read"


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
    )
    status: Mapped[Enum] = mapped_column(
        default=BookStatus.TO_READ,
    )

    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="user_details",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="book_details",
    )
