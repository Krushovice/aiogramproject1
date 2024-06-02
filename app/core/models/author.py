from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .book import Book


class Author(Base):
    __tablename__ = "authors"

    full_name: Mapped[str] = mapped_column(String(150))
    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(Author(id={self.id!r}, first_name={self.full_name!r})"

    def __repr__(self):
        return str(self)
