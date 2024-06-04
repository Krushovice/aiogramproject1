from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    Integer,
    UniqueConstraint,
)

from .base import Base


# Промежуточная таблица для прочитанных книг
user_books_table = Table(
    "user_books",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
    ),
    Column(
        "book_id",
        ForeignKey("books.id", ondelete="CASCADE"),
    ),
    UniqueConstraint("user_id", "book_id", name="idx_unique_user"),
)

# Промежуточная таблица для списка желаемого
user_wishlist_table = Table(
    "user_wishlist",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
    ),
    Column(
        "book_id",
        ForeignKey("books.id", ondelete="CASCADE"),
    ),
    UniqueConstraint("user_id", "book_id", name="idx_unique_user"),
)
