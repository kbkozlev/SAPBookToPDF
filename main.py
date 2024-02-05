import os
import shutil
from selenium import webdriver
from src.cropPictures import crop_images
from src.createBackup import create_backup
from src.getPictures import get_book_pages
from src.sharpenPictures import sharpen_images_in_folder
from src.compressPictures import compress_pictures
from src.helper.isPresent import is_present
from src.helper.initDriver import init_driver
from src.helper.initBooks import init_books
from src.helper.bookDataBase import remove_book_from_db


def process_book_images(book_url: str, name: str, cover: str, drv: webdriver.Edge, i: int, total: int) -> bool:
    """
    For each book, handles the processing in a predefined sequence.
    :param cover: The URL for the book
    :param book_url: The URL to the book to be processed
    :param name: The name of the book, used also for archive name
    :param drv: Driver object
    :param i: Index of the current book in the list
    :param total: The total number of books in the list
    :return:
    """
    output_folder = ''

    steps = [
        ("Capturing book pages", lambda: get_book_pages(book_url=book_url, cover=cover, driver=drv)),
        ("Cropping images", lambda: crop_images(input_folder=output_folder, size=size)),
        ("Sharpening images", lambda: sharpen_images_in_folder(input_folder=output_folder)),
        ("Compressing images", lambda: compress_pictures(input_folder=output_folder)),
        ("Creating backup", lambda: create_backup(input_folder=output_folder, out_name=name)),
    ]

    print(f"\nBook [ {i} | {total} ]: '{name}' started processing.")

    for step_name, step_function in steps:
        if step_name == 'Capturing book pages':
            ok, output_folder, size = step_function()
        else:
            ok, output_folder = step_function()

        if not ok:
            print(f"\nStep '{step_name}': failed.")
            return False

    remove_directories()
    remove_book_from_db(title=name)
    print(f"\nBook [ {i} | {total} ]: '{name}' finished processing.")
    return True


def remove_directories() -> None:
    """
    Handles the cleanup of the directories used for the processing of the images
    :return:
    """
    for dir_entry in os.listdir('files'):
        dir_full_path = os.path.join('files', dir_entry)

        if os.path.isdir(dir_full_path):
            try:
                shutil.rmtree(dir_full_path)
                print(f"Directory '{dir_entry}' successfully removed.")
            except OSError as e:
                print(f"\nError: {dir_entry} : {e.strerror}")


def main() -> None:
    """
    1. Checks for entered credentials
    2. Fetches a list of all books
    3. Iterates over the list to fetch and process all images/pages of a book
    :return:
    """
    all_present, login_data = is_present()

    if not all_present:
        return

    with init_driver() as driver:
        email, passwd = login_data
        success, book_list = init_books(e_mail=email, passwd=passwd, driver=driver)

        if not success:
            return

        for index, book in enumerate(book_list, start=1):
            title, url, cover = book['title'], book['href'], book['cover']
            finished = process_book_images(book_url=url, name=title, cover=cover, drv=driver, i=index, total=len(book_list))

            if not finished:
                print(f"\nBook processing terminated for book: '{title}'")
                return

        print("\nAll Books were processed successfully!")


if __name__ == '__main__':
    main()
