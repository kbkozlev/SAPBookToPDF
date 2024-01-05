import os
import shutil
import subprocess


def compress_images(input_folder) -> tuple[bool, str] | tuple[bool, None]:
    pngquant_path = 'src/pngquant/pngquant.exe'
    output_folder = 'files/finalPictures/'

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

        print(f'All Pictures processed and saved in folder {output_folder}')
        return True, output_folder

    except Exception as e:
        print(f"Error during compression: {e}")
        return False, None
