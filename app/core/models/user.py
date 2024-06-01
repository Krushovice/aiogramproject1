from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import BigInteger

from .base import Base
from .book import Book


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(User(id={self.id!r}, name={self.first_name!r}, fullname={self.last_name!r})"

    def __repr__(self):
        return str(self)
