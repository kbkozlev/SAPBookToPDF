from PIL import Image
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor


def __crop_image(args):
    image_path, output_path, coordinates = args
    try:
        with Image.open(image_path) as img:
            cropped_image = np.array(img.crop(coordinates))
            Image.fromarray(cropped_image).save(output_path)
        print(f"Image '{os.path.basename(image_path)}' cropped.")
        return True
    except Exception as e:
        print(f"Error cropping '{os.path.basename(image_path)}': {e}")
        return False


def crop_images(input_folder, size):
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
            print(f"\nAll pictures have been cropped and saved to folder '{output_folder}'.\n")

        return all_successful, output_folder
    else:
        print(f"\nNo Files in '{input_folder}'.\n")
        return False, None
