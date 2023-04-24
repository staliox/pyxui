from typing import Any

import xui
from xui import errors

class Login:
    def login(self: "xui.XUI", username: str, password: str) -> Any:
        _send_request = self.request("login", {
            'username': username,
            'password': password
        })

        if _send_request.status_code == 200:
            self.session_string = _send_request.cookies.get("session")
            print(self.session_string)

            try:
                self.get_inbounds()
            except errors.NotFound:
                raise errors.BadLogin()

            return True
        else:
            raise errors.BadLogin()