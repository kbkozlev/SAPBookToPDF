from PIL import Image
import os


def crop_images(input_folder: str) -> tuple[bool, str] | tuple[bool, None]:
    """
    Crops images from the input folder based on coordinates and saves cropped images to the output folder.
    :param input_folder:
    :return:
    """
    coordinates = (482, 282, 2490, 3182)

    # Create output folder if it doesn't exist
    output_folder = 'files/2.croppedPictures'
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    if len(files) > 0:
        for filename in files:
            try:
                input_image_path = os.path.join(input_folder, filename)
                output_image_path = os.path.join(output_folder, filename)

                with Image.open(input_image_path) as image:
                    image.crop(coordinates).save(output_image_path)

                print(f"Image '{filename}' cropped.")

            except Exception as e:
                print(f"Error: {e}")
                return False, None

        print(f"\nAll pictures have been cropped and saved to folder '{output_folder}'.\n")
        return True, output_folder

    else:
        print(f"\nNo Files in '{input_folder}'.\n")
        return False, None
