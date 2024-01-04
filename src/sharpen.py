import os
import cv2
import numpy as np
import shutil


def sharpen_images_in_folder():
    output_folder = 'files/sharpenedPictures'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_folder = 'files/croppedPictures'
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
                print(f"Unable to save processed image '{file_name}'. Copied original instead.")
            else:
                print(f"Image '{file_name}' sharpened.")
        else:
            print(f"Unable to read '{file_name}'")
            return False  # Return False if any image failed to read

    return True  # Return True if all images processed successfully
