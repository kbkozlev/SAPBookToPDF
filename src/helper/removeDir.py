import os
import shutil


def remove_directories() -> None:
    """
    Handles the cleanup of the directories used for the processing of the images
    :return:
    """
    for dir_entry in os.listdir('files'):
        dir_full_path = os.path.join('files', dir_entry)

        if os.path.isdir(dir_full_path):
            try:
                shutil.rmtree(dir_full_path)
                print(f"Directory '{dir_entry}' successfully removed.")
            except OSError as e:
                print(f"\nError: {dir_entry} : {e.strerror}")
