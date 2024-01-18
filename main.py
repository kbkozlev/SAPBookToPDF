import os
from send2trash import send2trash
from src.cropPictures import crop_images
from src.createBackup import create_backup
from src.getPictures import init_books, get_book_pages
from src.sharpenPictures import sharpen_images_in_folder
from src.compressPictures import compress_pictures
from src.helper.isPresent import is_present, args_dict


def process_book_images(book_url: str, name: str) -> bool:
    output_folder = ''

    steps = [
        ("Capturing book pages", lambda: get_book_pages(book_url)),
        ("Cropping images", lambda: crop_images(output_folder)),
        ("Sharpening images", lambda: sharpen_images_in_folder(output_folder)),
        ("Compressing images", lambda: compress_pictures(output_folder)),
        ("Creating backup", lambda: create_backup(output_folder, name)),
    ]

    print(f"\nBook: {name} started processing")

    for step_name, step_function in steps:
        success, output_folder = step_function()
        if not success:
            print(f"Step '{step_name}': Failed")
            return False

    print(f"\nBook: {name} finished processing!")
    return True


def remove_directories():
    for dir_entry in os.listdir('files'):
        dir_full_path = os.path.join('files', dir_entry)

        if os.path.isdir(dir_full_path):
            try:
                send2trash(dir_full_path)
                print(f"Directory '{dir_entry}' successfully removed.")
            except OSError as e:
                print(f"Error: {dir_entry} : {e.strerror}")


if __name__ == '__main__':

    all_present, present_arguments = is_present(**args_dict)

    if all_present:
        email, passwd = present_arguments
        suc, book_list = init_books(e_mail=email, passwd=passwd)

        if suc:
            for book in book_list:
                title, url = book['title'], book['href']
                processing_successful = process_book_images(book_url=url, name=title)

                if processing_successful:
                    remove_directories()

            print("\nAll Books were processed successfully!")
        else:
            print("No Books Found!")
