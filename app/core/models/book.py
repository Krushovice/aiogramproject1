from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .author import Author


class Book(Base):
    __tablename__ = "books"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    genre: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    user: Mapped["User"] = relationship(
        back_populates="books",
    )

    author: Mapped["Author"] = relationship(
        back_populates="books",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, author={self.author!r})"

    def __repr__(self):
        return str(self)
