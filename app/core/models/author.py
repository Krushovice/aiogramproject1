from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .book import Book


class Author(Base):
    __tablename__ = "authors"

    first_name: Mapped[str]
    last_name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(Author(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

    def __repr__(self):
        return str(self)
