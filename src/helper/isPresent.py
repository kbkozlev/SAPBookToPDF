from src.helper.createIniFile import create_ini_file, get_credentials

create_ini_file()
email, password = get_credentials()


def is_present(**kwargs) -> tuple:
    present = True
    present_args = []

    for arg_name, arg_value in kwargs.items():
        if len(arg_value) == 0:
            print(f"{arg_name}: is empty.")
            present = False
        else:
            present_args.append(arg_value)

    return present, present_args


args_dict = {
    'E-mail': email,
    'Password': password,
}
