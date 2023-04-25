from typing import Any

import xui
from xui import errors

class Login:
    def login(
        self: "xui.XUI",
        username: str,
        password: str
    ) -> Any:
        """Login into xui panel.

<<<<<<< HEAD
        Parameters:
            username (``str``):
                Username of panel
                
            password (``str``):
                Password of panel

        Returns:
            `~Any`: On success, True is returned else an error will be raised
        """
        
        if self.session_string:
            raise errors.AlreadyLogin()
        
        send_request = self.request(
            path="login",
            method="GET",
            params={
                'username': username,
                'password': password
            }
        )

        if send_request.status_code == 200:
            self.session_string = send_request.cookies.get("session")

=======
        if _send_request.status_code == 200:
            self.session_string = _send_request.cookies.get("session")

>>>>>>> 3c5a0c91d28d9de6b5919a3391055ae670ccfbe7
            if self.session_string:
                return True
            else:
                raise errors.BadLogin()

        else:
            raise errors.BadLogin()
