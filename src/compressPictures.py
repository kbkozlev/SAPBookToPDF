import os
import shutil
from PIL import Image, UnidentifiedImageError
from concurrent.futures import ProcessPoolExecutor
from advancedprinter import print


def __compress_picture(args: list):
    """
    Private function, handles the compression of the images
    :param args: Tuple of the input and output paths
    :return:
    """
    input_path, output_path = args

    if os.path.basename(input_path) == "00.png":  # Skip if the name of the pic is 00.png - e.g. the cover
        shutil.copyfile(input_path, output_path)
        print(f"Image '{os.path.basename(input_path)}' copied.")

    else:
        try:
            with Image.open(input_path) as img:
                output_path = os.path.splitext(output_path)[0] + ".jpg"  # Use the .jpg extension
                img.convert("RGB").save(output_path, 'JPEG', optimize=True)
                print(f"Image '{os.path.basename(input_path)}' compressed.")

        except UnidentifiedImageError as uie:
            print(f"Failed to compress image '{os.path.basename(input_path)}' due to UnidentifiedImageError: {uie}", c='red')
            print(f"Copying original!", c='red')
            shutil.copyfile(input_path, output_path)

        except Exception as e:
            print(f"Failed to compress image '{os.path.basename(input_path)}' with an unexpected error: {e}", c='red')
            print('Copying original!', c='red')
            shutil.copyfile(input_path, output_path)


def compress_pictures(input_folder: str) -> tuple[bool, str]:
    """
    Handles the compression of all images in the provided input folder.
    :param input_folder: Path to the input folder
    :return:
    """
    # Create output folder if it doesn't exist
    output_folder = 'files/4.finalPictures/'
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    with ProcessPoolExecutor() as executor:
        input_output_paths = [(os.path.join(input_folder, filename), os.path.join(output_folder, filename)) for filename in files]
        executor.map(__compress_picture, input_output_paths)

    print(f'\nAll pictures have been compressed and saved to folder {output_folder}\n', c='green2')
    return True, output_folder
