import py7zr
import os


def create_backup(input_folder, out_name) -> tuple[bool, str] | tuple[bool, None]:

    # Check if the folder exists
    if not os.path.exists(input_folder):
        print(f"Folder '{input_folder}' does not exist.")
        return False, None

    output_name = f"files/{out_name}.7z"

    # Get a list of files in the folder and sort them numerically
    files = os.listdir(input_folder)
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    # Create a 7z archive
    if len(files) > 0:
        with py7zr.SevenZipFile(output_name, 'w') as archive:
            # Add sorted files to the archive
            for file in files:
                file_path = os.path.join(input_folder, file)
                print(f"Adding '{file}' to archive")
                archive.write(file_path, os.path.relpath(file_path, input_folder))

        print(f"Folder '{input_folder}' successfully compressed to '{output_name}'.")
        return True, input_folder

    else:
        print(f"No Files in '{input_folder}', nothing to archive")
        return False, None
