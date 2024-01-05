import os
import configparser

file_path = 'src/helper/info.ini'


def create_ini_file():
    if not os.path.exists(file_path):
        config = configparser.ConfigParser()
        config['Credentials'] = {
            'Email': '',
            'Password': ''
        }
        config['Book'] = {
            'Book ID': '',
            'Archive Name': 'Archive'
        }

        with open(file_path, 'w') as configfile:
            config.write(configfile)
        print("INI file with empty credentials created successfully.")
        return False
    return True


def get_credentials():
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


def get_book_id():
    if os.path.exists(file_path):
        config = configparser.ConfigParser()
        config.read(file_path)

        book = config['Book'] if 'Book' in config else None
        if book:
            book_id = book.get('Book ID')
            arch_name = book.get('Archive Name')
            return book_id, arch_name

        print("No 'Book' section found in the INI file.")
        return None

    print("INI file 'info.ini' does not exist.")
    return None
