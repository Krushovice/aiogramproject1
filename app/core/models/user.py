from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import BigInteger, String


from .base import Base, user_books_table, user_wishlist_table


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        default=str(tg_id),
    )

    books = relationship(
        "Book",
        secondary=user_books_table,
        back_populates="readers",
        lazy="selectin",
    )

    wish_list = relationship(
        "Book",
        secondary=user_wishlist_table,
        back_populates="wishers",
        lazy="selectin",
    )

    def __str__(self):
        return f"User(id={self.id!r}, full_name={self.full_name!r})"

    def __repr__(self) -> str:
        return str(self)
