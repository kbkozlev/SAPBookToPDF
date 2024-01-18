import os
from send2trash import send2trash
from src.cropPictures import crop_images
from src.createBackup import create_backup
from src.getPictures import get_book_pages
from src.sharpenPictures import sharpen_images_in_folder
from src.compressPictures import compress_pictures
from src.helper.isPresent import is_present
from src.helper.innitDriver import innit_driver
from src.helper.innitBooks import init_books


def process_book_images(book_url: str, name: str, drv, i: int, total: int) -> bool:
    output_folder = ''

    steps = [
        ("Capturing book pages", lambda: get_book_pages(book_url, driver=drv)),
        ("Cropping images", lambda: crop_images(output_folder)),
        ("Sharpening images", lambda: sharpen_images_in_folder(output_folder)),
        ("Compressing images", lambda: compress_pictures(output_folder)),
        ("Creating backup", lambda: create_backup(output_folder, name)),
    ]

    print(f"\nBook [ {i} | {total} ]: '{name}' started processing")

    for step_name, step_function in steps:
        ok, output_folder = step_function()
        if not ok:
            print(f"\nStep '{step_name}': Failed")
            return False

    print(f"\nBook [ {i} | {total} ]: '{name}' finished processing!")
    return True


def remove_directories():
    for dir_entry in os.listdir('files'):
        dir_full_path = os.path.join('files', dir_entry)

        if os.path.isdir(dir_full_path):
            try:
                send2trash(dir_full_path)
                print(f"Directory '{dir_entry}' successfully removed.")
            except OSError as e:
                print(f"\nError: {dir_entry} : {e.strerror}")


def main():
    all_present, login_data = is_present()
    if not all_present:
        return

    with innit_driver() as driver:
        email, passwd = login_data
        success, book_list = init_books(e_mail=email, passwd=passwd, driver=driver)

        if success:
            for index, book in enumerate(book_list, start=1):
                title, url = book['title'], book['href']
                processing_successful = process_book_images(book_url=url, name=title, drv=driver, i=index,
                                                            total=len(book_list))

                if processing_successful:
                    remove_directories()

            print("\nAll Books were processed successfully!")


if __name__ == '__main__':
    main()
