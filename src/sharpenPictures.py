import os
import cv2
import numpy as np
import shutil


def sharpen_images_in_folder(input_folder: str) -> tuple[bool, str] | tuple[bool, None]:
    """
    Uses a kernel to sharpen the images
    :param input_folder:
    :return:
    """
    # Create output folder if it doesn't exist
    output_folder = 'files/3.sharpenedPictures'
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Get a list of files in the folder and sort them numerically
        files = os.listdir(input_folder)
        files.sort(key=lambda x: int(os.path.splitext(x)[0]))

        for file_name in files:
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

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
                    print(f"\nUnable to save processed image '{file_name}'. Copied original instead.")
                else:
                    print(f"Image '{file_name}' sharpened.")
            else:
                raise FileNotFoundError(f"\nUnable to read '{file_name}'. The image file may be missing or corrupted.")

        print(f"\nAll pictures have been sharpened and saved to folder '{output_folder}'.\n")
        return True, output_folder

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False, None
