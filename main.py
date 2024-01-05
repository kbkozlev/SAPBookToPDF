from src.cropPic import crop_images
from src.zip_backup import create_backup
from src.seleniumImage import capture_book_pages
from src.sharpen import sharpen_images_in_folder
from src.compress import compress_png_folder
from src.helper.credentials import create_cred_file, get_credentials


def process_book_images(e_mail: str, passwd: str, book_url: str, backup_name: str) -> bool:
    # Step 1: Capture book pages
    capture_success, cap_out_dir = capture_book_pages(e_mail, passwd, book_url)

    if not capture_success:
        print("Step 1 (Capturing book pages): Failed")
        return False

    # Step 2: Crop images
    crop_success, crop_out_dir = crop_images(input_folder=cap_out_dir)
    if not crop_success:
        print("Step 2 (Cropping images): Failed")
        return False

    # Step 3: Create backup
    backup_success = create_backup(input_folder=crop_out_dir, out_name=backup_name)
    if not backup_success:
        print("Step 3 (Creating backup): Failed")
        return False

    # Step 4: Sharpen images
    sharpen_success, sharp_out_dir = sharpen_images_in_folder(input_folder=crop_out_dir)
    if not sharpen_success:
        print("Step 4 (Sharpening images): Failed")
        return False

    # Step 5: Compress images
    compress_png_folder(input_folder=sharp_out_dir)
    print("All steps completed successfully!")
    return True


if __name__ == '__main__':
    create_cred_file()
    email, password = get_credentials()
    if email and password:
        process_book_images(e_mail=email, passwd=password, book_url="https://library.sap-press.com/reader/main/rhes-g69t-27nu-b8xd/",
                            backup_name='pictureBackup')
