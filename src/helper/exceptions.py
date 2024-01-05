class LoginFailedError(Exception):
    def __init__(self, message="Login failed!"):
        self.message = message
        super().__init__(self.message)
