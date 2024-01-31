import os
import shutil
from PIL import Image, UnidentifiedImageError
from concurrent.futures import ProcessPoolExecutor


def __compress_picture(path_tuple: tuple):
    """
    Private function, handles the compression of the images
    :param path_tuple: Tuple of the input and output paths
    :return:
    """
    input_path, output_path = path_tuple
    try:
        with Image.open(input_path) as img:
            img.convert("RGB").save(output_path, 'JPEG', optimize=True)
            print(f"Image '{os.path.basename(input_path)}' compressed.")
    except UnidentifiedImageError as uie:
        print(f"Failed to compress image '{os.path.basename(input_path)}' due to UnidentifiedImageError: {uie}\nCopying original!")
        shutil.copyfile(input_path, output_path)
    except Exception as e:
        print(f"Failed to compress image '{os.path.basename(input_path)}' with an unexpected error: {e}\nCopying original!")
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

    print(f'\nAll pictures have been compressed and saved to folder {output_folder}\n')
    return True, output_folder
