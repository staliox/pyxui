class Exceptions(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

class NotFound(Exceptions):
    code = 'NOT_FOUND'
    message = 'Error 404 has been received'

    def __init__(self):
        super().__init__(self.message, self.code)

    def __str__(self):
        return f"[{self.code}] {self.message}."

class BadLogin(Exceptions):
    code = 'BAD_LOGIN'
    message = 'Username or password is incorrect'

    def __init__(self):
        super().__init__(self.message, self.code)

    def __str__(self):
        return f"[{self.code}] {self.message}."

class AlreadyLogin(Exceptions):
    code = 'ALREADY_LOGIN'
    message = 'You are currently logged in'

    def __init__(self):
        super().__init__(self.message, self.code)

    def __str__(self):
        return f"[{self.code}] {self.message}."