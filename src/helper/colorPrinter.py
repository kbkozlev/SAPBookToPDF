class Color:
    class C:
        RESET = '\033[0m'
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'

    @classmethod
    def red(cls, text):
        return cls.C.RED + text + cls.C.RESET

    @classmethod
    def green(cls, text):
        return cls.C.GREEN + text + cls.C.RESET

    @classmethod
    def yellow(cls, text):
        return cls.C.YELLOW + text + cls.C.RESET

    @classmethod
    def blue(cls, text):
        return cls.C.BLUE + text + cls.C.RESET

    @classmethod
    def purple(cls, text):
        return cls.C.PURPLE + text + cls.C.RESET

    @classmethod
    def cyan(cls, text):
        return cls.C.CYAN + text + cls.C.RESET
