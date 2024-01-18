import os
import configparser

file_path = 'src/helper/info.ini'


def create_ini_file():
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
        print("INI file with empty credentials created successfully.")
        return False
    return True


def get_credentials():
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

        print("No 'Credentials' section found in the INI file.")
        return None, None

    print("INI file 'info.ini' does not exist.")
    return None, None
