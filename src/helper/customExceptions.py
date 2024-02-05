class LoginFailedError(Exception):
    """
    Custom class for raising an error when the login fails
    """
    def __init__(self, message="Login failed!"):
        self.message = message
        super().__init__(self.message)


class IdenticalImageError(Exception):
    """
    Custom class for raising an error when the last two images are identical
    """
    def __init__(self, message="Last two images are identical"):
        self.message = message
        super().__init__(self.message)
