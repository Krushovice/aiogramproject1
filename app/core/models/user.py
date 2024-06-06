from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import BigInteger, String
from typing import TYPE_CHECKING, List


from .base import Base

if TYPE_CHECKING:
    from .user_book_association import UserBookAssociation
    from .book import Book


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        default=str(tg_id),
    )
    favourite_genre: Mapped[str] = mapped_column(String(25), nullable=True)

    book_details: Mapped[List["UserBookAssociation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    # books: Mapped[List["Book"]] = relationship(
    #     secondary="user_book_association", back_populates="users"
    # )

    def __str__(self):
        return f"User(id={self.id!r}, full_name={self.full_name!r})"

    def __repr__(self) -> str:
        return str(self)
