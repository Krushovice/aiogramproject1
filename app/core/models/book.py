from sqlalchemy import Text, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base, user_books_table, user_wishlist_table


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)
    author: Mapped[str] = mapped_column(String(150), nullable=False)

    readers = relationship(
        "User",
        secondary=user_books_table,
        back_populates="books",
        lazy="selectin",
    )

    wishers = relationship(
        "User",
        secondary=user_wishlist_table,
        back_populates="wish_list",
        lazy="selectin",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.title!r}, author={self.author!r})"

    def __repr__(self):
        return str(self)
