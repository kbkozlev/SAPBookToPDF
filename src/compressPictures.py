import os
import shutil
from PIL import Image, UnidentifiedImageError
from concurrent.futures import ProcessPoolExecutor


def __compress_picture(input_path, output_path):
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
    # Create output folder if it doesn't exist
    output_folder = 'files/4.finalPictures/'
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    with ProcessPoolExecutor() as executor:
        futures = []
        for filename in files:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            futures.append(executor.submit(__compress_picture, input_path, output_path))

        # Wait for all futures to complete
        for future in futures:
            future.result()

    print(f'\nAll pictures have been compressed and saved to folder {output_folder}\n')
    return True, output_folder
