import py7zr
import os


def compress_folder_to_7z(input_folder, output_name):

    # Check if the folder exists
    if not os.path.exists(input_folder):
        print(f"Folder '{input_folder}' does not exist.")
        return

    output_7z_file = f"{output_name}.7z"

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    # Create a 7z archive
    if len(files) > 0:
        with py7zr.SevenZipFile(output_7z_file, 'w') as archive:
            # Add sorted files to the archive
            for file in files:
                file_path = os.path.join(input_folder, file)
                print(f"Adding {file} to archive")
                archive.write(file_path, os.path.relpath(file_path, input_folder))

        print(f"Folder '{input_folder}' successfully compressed to '{output_name}.7z'.")

    else:
        print(f"No Files in {input_folder}, nothing to archive")
        return False
