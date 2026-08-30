class Exceptions(Exception):
    code = 'UNKNOWN'
    message = 'An unknown error has occurred'

    def __init__(self, message: str = None, error_code: str = None):
        self.message = message or self.message
        self.error_code = error_code or self.code
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.error_code}] {self.message}."

class NotFound(Exceptions):
    code = 'NOT_FOUND'
    message = 'Error 404 has been received'

class BadLogin(Exceptions):
    code = 'BAD_LOGIN'
    message = 'Username or password is incorrect'

class AlreadyLogin(Exceptions):
    code = 'ALREADY_LOGIN'
    message = 'You are currently logged in'

class NotLogin(Exceptions):
    code = 'NOT_LOGIN'
    message = 'You are not logged in, call login() first'

class BadResponse(Exceptions):
    code = 'BAD_RESPONSE'
    message = 'The panel returned a response that could not be parsed'

class BadMethod(Exceptions):
    code = 'BAD_METHOD'
    message = 'Only GET and POST methods are supported'

class UnsupportedPanel(Exceptions):
    code = 'UNSUPPORTED_PANEL'
    message = 'Panel must be either "alireza" or "sanaei"'

class RequestError(Exceptions):
    code = 'REQUEST_ERROR'
    message = 'The request to the panel has failed'

class PanelError(Exceptions):
    code = 'PANEL_ERROR'
    message = 'The panel rejected the request'
