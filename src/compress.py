import os
import subprocess


def compress_png_folder():
    pngquant_path = 'C:/Users/kbkoz/Downloads/pngquant-windows/pngquant/pngquant.exe'

    # Ensure the output folder exists, create if not
    output_folder = '../files/compressedPictures/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each file in the input folder
    input_folder = 'files/finalPictures/'
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            subprocess.run([pngquant_path, "--force", "--output", output_path, input_path])
