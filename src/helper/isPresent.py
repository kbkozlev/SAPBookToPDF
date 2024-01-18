from src.helper.createIniFile import create_ini_file, get_credentials


def is_present() -> tuple:
    create_ini_file()
    email, password = get_credentials()

    args_dict = {'E-mail': email, 'Password': password}
    present_args = [arg_value for arg_name, arg_value in args_dict.items() if len(arg_value) == 0]

    if present_args:
        for arg_name in present_args:
            print(f"{arg_name}: is empty.")
        return False, []
    else:
        return True, list(args_dict.values())