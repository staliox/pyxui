from typing import Any

import pyxui
from pyxui import errors

class Login:
    async def login(
        self: "pyxui.XUI",
        username: str,
        password: str,
        secret: str = None,
        force: bool = False
    ) -> Any:
        """Login into xui panel.

        Parameters:
            username (``str``):
                Username of panel

            password (``str``):
                Password of panel

            secret (``str``, optional):
                Two factor secret, only used by 3x-ui when it's enabled

            force (``bool``, optional):
                Login again even if a session already exists

        Returns:
            `~Any`: On success, True is returned else an error will be raised
        """

        if self.session_string and not force:
            raise errors.AlreadyLogin()

        params = {'username': username, 'password': password}

        if secret:
            params['loginSecret'] = secret

        send_request = await self.request(
            path="login",
            method="POST",
            params=params
        )

        if send_request.status == 200:
            session_string = send_request.cookies.get(self.cookie_name)

            if session_string:
                self.session_string = session_string
                self.clear_cache()

                if self.auto_relogin:
                    self._credentials = (username, password, secret)

                return True

        raise errors.BadLogin()

    async def relogin(self: "pyxui.XUI") -> bool:
        """Refresh an expired session using the stored credentials.

        Concurrent callers share a single login request.

        Returns:
            `~bool`: True when a new session was obtained, False when
            auto re-login is disabled or no credentials are known.
        """

        if not self.auto_relogin or not self._credentials:
            return False

        expired = self.session_string

        async with self._login_lock:
            if self.session_string and self.session_string != expired:
                return True

            self.session_string = None
            username, password, secret = self._credentials

            try:
                return await self.login(
                    username=username,
                    password=password,
                    secret=secret,
                    force=True
                )
            except errors.BadLogin:
                return False

    async def logout(self: "pyxui.XUI") -> None:
        """Drop the local session and the stored credentials."""

        self.session_string = None
        self._credentials = None
        self.clear_cache()
