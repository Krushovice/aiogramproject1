from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import BigInteger, String
from typing import TYPE_CHECKING


from .base import Base

if TYPE_CHECKING:
    from .user_book_association import UserBookAssociation


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        default=str(tg_id),
    )
    favorite_genre: Mapped[str] = mapped_column(String(25), nullable=True)

    books_details: Mapped[list["UserBookAssociation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"User(id={self.id!r}, full_name={self.full_name!r})"

    def __repr__(self) -> str:
        return str(self)
