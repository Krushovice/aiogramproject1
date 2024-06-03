from typing import TYPE_CHECKING
import operator
from collections import defaultdict


from core import Book


# books = [
#     Book(id=1, title='Идиот', author='Фёдор Достоевский', genre='noval'),
#     Book(id=3, title='Шантарам', author='Греггори Робертс', genre='noval'),
#     Book(id=23, title='1984', author='Джордж Оруэл', genre='story'),
#     Book(id=17, title='Оно', author='Стивен Кинг', genre='horror'),
#     Book(id=9, title='Грозовой перевал', author='Шарлотта Блонте', genre='Action')
# ]


def get_most_common_genre(book_list: list[Book]) -> str:
    genres = defaultdict(int)
    for book in book_list:
        genre = book.genre
        genres[genre] += 1
    return max(genres.items(), key=operator.itemgetter(1))[0]


