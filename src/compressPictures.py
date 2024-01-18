import os
import shutil
import subprocess


def compress_pictures(input_folder: str) -> tuple[bool, str] | tuple[bool, None]:
    """
    Uses a binary of "pngquant" to compress the images
    :param input_folder:
    :return:
    """
    pngquant_path = 'src/helper/pngquant/pngquant.exe'
    output_folder = 'files/4.finalPictures/'

    try:
        os.makedirs(output_folder, exist_ok=True)

        files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')], key=lambda x: int(os.path.splitext(x)[0]))

        for filename in files:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            result = subprocess.run([pngquant_path, "--force", "--output", output_path, input_path])
            if result.returncode != 0:
                print(f"Failed to compress image '{filename}', copying original.")
                shutil.copyfile(input_path, output_path)
            else:
                print(f"Image '{filename}' compressed.")

        print(f'\nAll pictures have been compressed and saved to folder {output_folder}\n')
        return True, output_folder

    except Exception as e:
        print(f"\nError during compression: {e}")
        return False, None
