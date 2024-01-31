import os
import shutil
from PIL import Image, UnidentifiedImageError


def compress_pictures(input_folder: str) -> tuple[bool, str]:
    """
    Uses PIL to compress the images
    :param input_folder:
    :return:
    """

    # Create output folder if it doesn't exist
    output_folder = 'files/4.finalPictures/'
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    for filename in files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            with Image.open(input_path) as img:
                img.convert("RGB").save(output_path, 'JPEG', optimize=True)
                print(f"Image '{filename}' compressed.")
        except UnidentifiedImageError as uie:
            print(f"Failed to compress image '{filename}' due to UnidentifiedImageError: {uie}\nCopying original!")
            shutil.copyfile(input_path, output_path)
        except Exception as e:
            print(f"Failed to compress image '{filename}' with an unexpected error: {e}\nCopying original!")
            shutil.copyfile(input_path, output_path)

    print(f'\nAll pictures have been compressed and saved to folder {output_folder}\n')
    return True, output_folder
