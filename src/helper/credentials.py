import os
import configparser


def create_cred_file():
    file_path = 'src/helper/credentials.ini'
    if not os.path.exists(file_path):
        config = configparser.ConfigParser()
        config['Credentials'] = {
            'Email': "''",  # Empty string within single quotes
            'Password': "''"  # Empty string within single quotes
        }

        with open(file_path, 'w') as configfile:
            config.write(configfile)
            print("INI file with empty credentials created successfully.")
            return False


def get_credentials():
    file_path = 'src/helper/credentials.ini'
    if os.path.exists(file_path):
        config = configparser.ConfigParser()
        config.read(file_path)

        # Check if the 'Credentials' section exists in the INI file
        if 'Credentials' in config:
            credentials = config['Credentials']

            # Fetch the email and password
            email = credentials.get('Email')
            password = credentials.get('Password')

            return email, password
        else:
            print("No 'Credentials' section found in the INI file.")
            return None, None
    else:
        print("INI file 'credentials.ini' does not exist.")
        return None, None
