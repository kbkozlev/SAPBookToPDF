import json
from src.helper.colorPrinter import Color

file_path = 'src/helper/files/books.json'


def create_db():
    """
    Creates an empty JSON Database file
    :return:
    """
    with open(file_path, 'w') as file:
        json.dump([], file)


def __load_data() -> list:
    """
    Loads the full JSON db and returns a list of dictionaries containing book information.
    :return:
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []
    return data


def __save_data(data: list[dict[str, str]]):
    """
    Save data to the JSON database file.
    :param data:
    :return:
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def insert_book_in_db(title: str, href: str, cover: str):
    """
    Insert new entry in the db.
    :param cover: Cover of the book
    :param title: The title of the book
    :param href: The URL to the book
    :return:
    """
    data = __load_data()
    data.append({'title': title, 'href': href, 'cover': cover})
    __save_data(data)


def remove_book_from_db(title: str):
    """
    Remove a book entry from the db
    :param title: The title of the book
    :return:
    """
    data = __load_data()
    updated_data = [book for book in data if book['title'] != title]
    __save_data(updated_data)
    print(Color.yellow(f"\nBook: '{title}' removed from db."))


def get_book_list_from_db() -> list:
    """
    Calls private method '__load_data' and returns it
    :return:
    """
    return __load_data()
