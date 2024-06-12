import requests

from core import settings


class BookInfo:
    def __init__(self, title, author, description, categories):
        self.title = title
        self.author = author
        self.description = description
        self.categories = categories


def get_book_info(title):
    endpoint = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": title,
        "maxResults": 3,
        "fields": "items(volumeInfo/title,volumeInfo/authors,volumeInfo/description,volumeInfo/categories)",  # noqa
        "key": settings.api_key,
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        data = response.json()
        if "items" in data:
            book_data = data["items"][0]["volumeInfo"]
            title = book_data.get("title", "Название неизвестно")
            author = book_data.get("authors", ["Автор неизвестен"])[0]
            description = book_data.get("description", "Описание отсутствует")[
                :255
            ]  # noqa
            categories = book_data.get("categories", ["Категория не указана"])[
                0
            ]  # noqa

            return BookInfo(title, author, description, categories)
        else:
            return BookInfo("Книга не найдена", "", "", [])
    except requests.HTTPError as e:
        return f"Ошибка HTTP при запросе к API: {e}"
    except Exception as ex:
        return f"Произошла ошибка: {ex}"


def update_books_info(books: list):
    if len(books) <= 1:
        updated_book = get_book_info(books[0])
        updated_book["title"] = books[0]
        return updated_book
    updated_books = []
    for book in books:
        updated_book = get_book_info(book)
        updated_book["title"] = book
        updated_books.append(updated_book)
        return updated_books
