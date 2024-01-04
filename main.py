from src.cropPic import crop_images
from src.zip_backup import create_backup
from src.seleniumImage import capture_book_pages
from src.sharpen import sharpen_images_in_folder
from src.compress import compress_png_folder

if __name__ == '__main__':

    capture_success = capture_book_pages(book_url="https://library.sap-press.com/reader/main/43ev-bc9p-szan-r8ty/")

    if capture_success:
        crop_success = crop_images()

        if crop_success:
            sharpen_success = sharpen_images_in_folder()

            if sharpen_success:
                compress_png_folder()

    create_backup()