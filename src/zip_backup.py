import py7zr
import os


def compress_folder_to_7z(folder_path, output_name):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    output_7z_file = f"{output_name}.7z"

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(folder_path)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    # Create a 7z archive
    with py7zr.SevenZipFile(output_7z_file, 'w') as archive:
        # Add sorted files to the archive
        for file in files:
            file_path = os.path.join(folder_path, file)
            print(f"Adding {file} to archive")
            archive.write(file_path, os.path.relpath(file_path, folder_path))

    print(f"Folder '{folder_path}' successfully compressed to '{output_name}.7z'.")
