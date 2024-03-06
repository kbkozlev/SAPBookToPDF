import os
import configparser
from advancedprinter import print

file_path = 'src/helper/files/info.ini'


def create_ini_file() -> bool:
    """
    Creates an INI file for storing credentials
    :return:
    """
    if not os.path.exists(file_path):
        config = configparser.ConfigParser()
        config['Credentials'] = {
            'Email': '',
            'Password': ''
        }

        with open(file_path, 'w') as configfile:
            config.write(configfile)
        print("INI file with empty credentials created successfully.", c='green2')
        return False
    return True


def get_credentials() -> tuple[str, str] | tuple[None, None]:
    """
    Fetches the credentials from the INI file
    :return:
    """
    if os.path.exists(file_path):
        config = configparser.ConfigParser()
        config.read(file_path)

        credentials = config['Credentials'] if 'Credentials' in config else None
        if credentials:
            email = credentials.get('Email')
            password = credentials.get('Password')
            return email, password

        print("No 'Credentials' section found in the INI file.", c='red')
        return None, None

    print("INI file 'info.ini' does not exist.", c='red')
    return None, None
