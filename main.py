import os
from send2trash import send2trash
from src.cropPic import crop_images
from src.zip_backup import create_backup
from src.seleniumImage import capture_book_pages
from src.sharpen import sharpen_images_in_folder
from src.compress import compress_images
from src.helper.credentials import create_ini_file, get_credentials, get_book


def process_book_images(e_mail: str, passwd: str, book_url: str, backup_name: str) -> bool:
    output_folder = ''

    steps = [
        ("Capturing book pages", lambda: capture_book_pages(e_mail, passwd, book_url)),
        ("Cropping images", lambda: crop_images(output_folder)),
        ("Sharpening images", lambda: sharpen_images_in_folder(output_folder)),
        ("Compressing images", lambda: compress_images(output_folder)),
        ("Creating backup", lambda: create_backup(output_folder, backup_name)),
    ]

    for step_name, step_function in steps:
        success, output_folder = step_function()
        if not success:
            print(f"Step '{step_name}': Failed")
            return False

    print("All steps completed successfully!")
    return True


def remove_directories():
    for dir_entry in os.listdir('files'):
        dir_full_path = os.path.join('files', dir_entry)

        if os.path.isdir(dir_full_path) and dir_entry != 'finalPictures':
            try:
                send2trash(dir_full_path)
                print(f"Directory '{dir_entry}' successfully removed.")
            except OSError as e:
                print(f"Error: {dir_entry} : {e.strerror}")


if __name__ == '__main__':
    create_ini_file()
    email, password = get_credentials()
    book = get_book()

    if email and password:
        processing_successful = process_book_images(e_mail=email, passwd=password, book_url=book, backup_name='pictureBackup')

        if processing_successful:
            remove_directories()
