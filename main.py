import os
from send2trash import send2trash
from src.cropPictures import crop_images
from src.createBackup import create_backup
from src.getPictures import capture_book_pages
from src.sharpenPictures import sharpen_images_in_folder
from src.compressPictures import compress_pictures
from src.helper.inPresent import is_present, args_dict


def process_book_images(e_mail: str, passwd: str, book_url: str, backup_name: str) -> bool:
    output_folder = ''

    steps = [
        ("Capturing book pages", lambda: capture_book_pages(e_mail, passwd, book_url)),
        ("Cropping images", lambda: crop_images(output_folder)),
        ("Sharpening images", lambda: sharpen_images_in_folder(output_folder)),
        ("Compressing images", lambda: compress_pictures(output_folder)),
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

    all_present, present_arguments = is_present(**args_dict)

    if all_present and len(present_arguments) == 4:
        email, passw, book, backup = present_arguments

        processing_successful = process_book_images(e_mail=email, passwd=passw, book_url=book, backup_name=backup)

        if processing_successful:
            remove_directories()
