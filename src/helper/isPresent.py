from src.helper.createIniFile import create_ini_file, get_credentials
from src.helper.colorPrinter import Color


def is_present() -> tuple[bool, list] | tuple[bool, None]:
    """
    Calls the function to create the INI file.
    Calls the function to fetch the credentials from the INI file.
    Checks if both the E-mail and Password are present in the INI file.
    :return: A tuple indicating whether the credentials are present and the list of credentials or None.
    """
    create_ini_file()
    email, password = get_credentials()

    if not email or not password:
        for arg_name, arg_value in {'E-mail': email, 'Password': password}.items():
            if not arg_value:
                print(f"{Color.red(f'{arg_name}: is empty.')}")
        return False, None

    return True, [email, password]
