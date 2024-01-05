from typing import Tuple

from PIL import Image
import os


def crop_images(input_folder) -> bool | tuple[bool, str]:
    """
    Crops images from the input folder based on coordinates and saves cropped images to the output folder.

    Args:
    input_folder: path to the folder containing input images.
    output_folder: path to save the cropped images.
    """
    coordinates = (463, 282, 2471, 3182)

    # Create output folder if it doesn't exist
    output_folder = 'files/croppedPictures'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    if len(files) > 0:
        for filename in files:
            try:
                if filename.endswith(('.png', '.jpg', '.jpeg')):  # Process only image files
                    input_image_path = os.path.join(input_folder, filename)
                    output_image_path = os.path.join(output_folder, filename)

                    image = Image.open(input_image_path)
                    cropped_image = image.crop(coordinates)
                    cropped_image.save(output_image_path)

                    print(f"Image '{filename}' has been cropped.")

            except Exception as e:
                print(f"Error: {e}")
                return False

        print(f"All pictures have been cropped and saved to folder '{output_folder}'.")
        return True, output_folder
    else:
        print(f"No Files in '{input_folder}'.")
        return False
