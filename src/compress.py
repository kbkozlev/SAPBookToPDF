import os
import subprocess


def compress_png_folder():
    pngquant_path = 'src/pngquant/pngquant.exe'

    # Ensure the output folder exists, create if not
    output_folder = 'files/finalPictures/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each file in the input folder
    input_folder = 'files/sharpenedPictures/'
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    for filename in files:
        if filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            subprocess.run([pngquant_path, "--force", "--output", output_path, input_path])
            print(f"Image '{filename}' compressed.")

    print(f"All Pictures compressed and saved in folder {output_folder}")