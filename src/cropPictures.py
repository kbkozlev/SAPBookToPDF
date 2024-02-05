import os
import shutil
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from src.helper.colorPrinter import Color


def __crop_image(args: list) -> bool:
    image_path, output_path, coordinates = args

    if os.path.basename(image_path) == "00.png":  # Skip if the name of the pic is 00.png - e.g. the cover
        shutil.copyfile(image_path, output_path)
        print(f"Image '{os.path.basename(image_path)}' copied.")
        return True

    else:
        try:
            with Image.open(image_path) as img:
                cropped_image = np.array(img.crop(coordinates))
                Image.fromarray(cropped_image).save(output_path)
                print(f"Image '{os.path.basename(image_path)}' cropped.")
                return True

        except Exception as e:
            print(f"""{Color.red(f"Error cropping '{os.path.basename(image_path)}': {e}")}""")
            return False


def crop_images(input_folder: str, size: int):
    """
    Handles the cropping of the picture, depending on the screenshot size.
    :param input_folder: Path to the input folder
    :param size: The size of the screenshot, taken from the 'get_book_pages' function
    :return:
    """
    coordinates = (0, 0, 0, 0)

    if size == 4:
        coordinates = (482, 282, 2490, 3182)
    elif size == 3:
        coordinates = (547, 282, 2417, 3182)

    output_folder = 'files/2.croppedPictures'
    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    if len(files) > 0:
        with ProcessPoolExecutor() as executor:
            args_list = [(os.path.join(input_folder, filename),
                          os.path.join(output_folder, filename),
                          coordinates) for filename in files]
            results = list(executor.map(__crop_image, args_list))

        all_successful = all(results)
        if all_successful:
            print(f"""\n{Color.green(f"All pictures have been cropped and saved to folder '{output_folder}'.")}\n""")

        return all_successful, output_folder

    else:
        print(f"""\n{Color.red(f"No Files in '{input_folder}'.")}\n""")
        return False, None
