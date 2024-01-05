from src.cropPic import crop_images
from src.zip_backup import create_backup
from src.seleniumImage import capture_book_pages
from src.sharpen import sharpen_images_in_folder
from src.compress import compress_png_folder

if __name__ == '__main__':

    # capture_success = capture_book_pages(book_url="https://library.sap-press.com/reader/main/rhes-g69t-27nu-b8xd/")
    #
    # if capture_success:
    #     crop_success = crop_images()
    #
    #     if crop_success:
    #         backup_success = create_backup()
    #
    #         if backup_success:
    #             sharpen_success = sharpen_images_in_folder()
    #
    #             if sharpen_success:
                    compress_png_folder()

