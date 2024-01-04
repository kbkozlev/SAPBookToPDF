from src.cropPic import crop_images
from src.zip_backup import compress_folder_to_7z
from src.seleniumImage import capture_book_pages

if __name__ == '__main__':

    capture_success = capture_book_pages(book_url="https://library.sap-press.com/reader/main/43ev-bc9p-szan-r8ty/")

    if capture_success:
        crop_success = crop_images(input_folder='src/rawPictures')

        if crop_success:
            compress_folder_to_7z(input_folder='src/croppedPictures', output_name='croppedPictures_backup')
