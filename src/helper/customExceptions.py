class LoginFailedError(Exception):
    """
    Custom class for raising an error when the login fails
    """
    def __init__(self, message="Login failed!"):
        self.message = message
        super().__init__(self.message)
