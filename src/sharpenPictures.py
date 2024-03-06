import os
import cv2
import numpy as np
import shutil
from concurrent.futures import ProcessPoolExecutor
from advancedprinter import print, line


def __sharpen_image(args: list) -> bool:
    """
    Private function, handles the sharpening of the images with a kernel.
    :param args: Tuple of input and output paths.
    :return:
    """
    input_path, output_path = args

    if os.path.basename(input_path) == "00.png":  # Skip if the name of the pic is 00.png - e.g. the cover
        shutil.copyfile(input_path, output_path)
        print(f"Image '{os.path.basename(input_path)}' copied.")
        return True

    else:
        try:
            img = cv2.imread(input_path)

            if img is not None:
                kernel = np.array([[0, -0.5, 0],
                                   [-0.5, 3, -0.5],
                                   [0, -0.5, 0]])

                sharpened = cv2.filter2D(img, -1, kernel)

                success = cv2.imwrite(output_path, sharpened)
                if not success:
                    # If unable to save, copy the original image instead
                    shutil.copyfile(input_path, output_path)
                    print(f"\nUnable to save processed image '{os.path.basename(input_path)}'. Copied original instead.", c='red')
                else:
                    print(f"Image '{os.path.basename(input_path)}' sharpened.")
            else:
                raise FileNotFoundError(f"""\n{line(f"Unable to read '{os.path.basename(input_path)}'. The image file may be missing or corrupted.", c='red')}""")

            return True

        except Exception as e:
            print(f'\nUnexpected error: {e}', c='red')
            return False


def sharpen_images_in_folder(input_folder: str) -> tuple[bool, str] | tuple[bool, None]:
    """
    Uses a kernel to sharpen the images.
    :param input_folder: Path to the input folder
    :return:
    """
    # Create output folder if it doesn't exist
    output_folder = 'files/3.sharpenedPictures'
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Get a list of files in the folder and sort them numerically
        files = os.listdir(input_folder)
        files.sort(key=lambda x: int(os.path.splitext(x)[0]))

        with ProcessPoolExecutor() as executor:
            args_list = [(os.path.join(input_folder, file_name),
                          os.path.join(output_folder, file_name)) for file_name in files]
            results = list(executor.map(__sharpen_image, args_list))

        all_successful = all(results)
        if all_successful:
            print(f"\nAll pictures have been sharpened and saved to folder '{output_folder}'.\n", c='green2')
        return all_successful, output_folder

    except Exception as e:
        print(f'\nUnexpected error: {e}', c='red')
        return False, None
