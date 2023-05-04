from typing import Any

import pyxui
from pyxui import errors

class Login:
    def login(
        self: "pyxui.XUI",
        username: str,
        password: str
    ) -> Any:
        """Login into xui panel.

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
            method="POST",
            params={
                'username': username,
                'password': password
            }
        )

        if send_request.status_code == 200:
            self.session_string = send_request.cookies.get("session")

            if self.session_string:
                return True
            else:
                raise errors.BadLogin()

        else:
            raise errors.BadLogin()
