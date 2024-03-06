import py7zr
import os
from advancedprinter import print, line


def create_backup(input_folder: str, out_name: str) -> tuple[bool, str] | tuple[bool, None]:
    """
    Creates a 7z backup of the processed images.
    :param input_folder:
    :param out_name: Name of the archive
    :return:
    """

    try:
        if not os.path.exists(input_folder):
            print(f"Folder '{input_folder}' does not exist.", c='red')
            return False, None

        output_name = f"files/{out_name}.7z"

        # Get a list of files in the folder and sort them numerically
        files = os.listdir(input_folder)
        files.sort(key=lambda x: int(os.path.splitext(x)[0]))

        # Create a 7z archive
        if len(files) > 0:
            with py7zr.SevenZipFile(output_name, 'w') as archive:
                for file in files:
                    file_path = os.path.join(input_folder, file)
                    archive.write(file_path, os.path.relpath(file_path, input_folder))
                    print(f"Image '{file}' archived")

            print(f"\nFolder '{input_folder}' successfully archived to '{output_name}'.", c='green2')
            return True, input_folder

        else:
            raise FileNotFoundError(f"""\n{line(f"No Files in '{input_folder}', nothing to archive.", c='red')}""")

    except Exception as e:
        print(f'\nUnexpected error: {e}', c='red')
        return False, None
