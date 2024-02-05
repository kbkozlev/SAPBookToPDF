class Color:
    """
    Utility class for generating colored text in the terminal using ANSI escape codes.
    """
    class C:
        """
        Nested class containing ANSI escape codes for different text colors.
        """
        RESET = '\033[0m'
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'

    @classmethod
    def red(cls, text: str) -> str:
        """
        Print text in red color.

        :param text: The text to be colored.
        :return: Colored text with red color.
        """
        return cls.C.RED + text + cls.C.RESET

    @classmethod
    def green(cls, text: str) -> str:
        """
        Print text in green color.

        :param text: The text to be colored.
        :return: Colored text with green color.
        """
        return cls.C.GREEN + text + cls.C.RESET

    @classmethod
    def yellow(cls, text: str) -> str:
        """
        Print text in yellow color.

        :param text: The text to be colored.
        :return: Colored text with yellow color.
        """
        return cls.C.YELLOW + text + cls.C.RESET

    @classmethod
    def blue(cls, text: str) -> str:
        """
        Print text in blue color.

        :param text: The text to be colored.
        :return: Colored text with blue color.
        """
        return cls.C.BLUE + text + cls.C.RESET

    @classmethod
    def purple(cls, text: str) -> str:
        """
        Print text in purple color.

        :param text: The text to be colored.
        :return: Colored text with purple color.
        """
        return cls.C.PURPLE + text + cls.C.RESET

    @classmethod
    def cyan(cls, text: str) -> str:
        """
        Print text in cyan color.

        :param text: The text to be colored.
        :return: Colored text with cyan color.
        """
        return cls.C.CYAN + text + cls.C.RESET
