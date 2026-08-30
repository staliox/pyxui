import json
import aiohttp
import asyncio
from typing import Any, Dict, Mapping, Union

import pyxui

from pyxui import errors

REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})

class Response:
    """A panel answer whose body has already been read.

    aiohttp streams responses and invalidates them as soon as the connection
    is released, so the body is consumed while the connection is still open
    and handed over in this small container.
    """

    __slots__ = ("status", "headers", "cookies", "body")

    def __init__(
        self,
        status: int,
        headers: Mapping[str, str],
        cookies: Dict[str, str],
        body: bytes
    ) -> None:
        self.status = status
        self.headers = headers
        self.cookies = cookies
        self.body = body

    @property
    def status_code(self) -> int:
        return self.status

    @property
    def content_type(self) -> str:
        return (self.headers.get("Content-Type") or "").split(";")[0].strip()

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", "replace")

    def json(self) -> Any:
        return json.loads(self.body)

    def __repr__(self) -> str:
        return f"<Response status={self.status}>"

class Base:
    async def get_session(self: "pyxui.XUI") -> aiohttp.ClientSession:
        """Return the shared ``aiohttp.ClientSession``, creating it on first use."""

        if self._session is not None and not self._session.closed:
            return self._session

        async with self._session_lock:
            if self._session is None or self._session.closed:
                self._session = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(
                        limit=self.max_connections,
                        ssl=True if self.verify_ssl else False,
                    ),
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    cookie_jar=aiohttp.DummyCookieJar(),
                    headers={"Accept": "application/json"},
                )
                self._owns_session = True

        return self._session

    def build_url(self: "pyxui.XUI", path: str) -> str:
        """Build the absolute panel url for the given endpoint.

        Built by hand rather than through ``ClientSession(base_url=...)``,
        which rejects any base that carries a path — panels served under a
        custom web base path would break.
        """

        if path == "login":
            return f"{self.full_address}/login"

        return f"{self.full_address}/{self.api_path}/inbounds/{path}"

    async def request(
        self: "pyxui.XUI",
        path: str,
        method: str = "GET",
        params: dict = None,
        retry_on_expire: bool = True
    ) -> Response:
        """Request to the xui panel.

        Parameters:
            path (``str``):
                The request path, you can see all of them in https://github.com/alireza0/x-ui#api-routes

            method (``str``):
                The request method, GET or POST

            params (``dict``, optional):
                The request parameters, None is set for default but it's necessary for some POST methods

            retry_on_expire (``bool``, optional):
                Re-login and replay the request once if the session has expired

        Returns:
            `~pyxui.methods.base.Response`: On success, the response is returned.
        """

        method = method.upper()

        if method not in ("GET", "POST"):
            raise errors.BadMethod(f'Unsupported method "{method}"')

        session = await self.get_session()
        url = self.build_url(path)
        cookies = {self.cookie_name: self.session_string} if self.session_string else None

        try:
            async with session.request(
                method,
                url,
                data=params if method == "POST" else None,
                cookies=cookies,
                allow_redirects=False
            ) as raw:
                response = Response(
                    status=raw.status,
                    headers=raw.headers,
                    cookies={key: morsel.value for key, morsel in raw.cookies.items()},
                    body=await raw.read()
                )
        except asyncio.TimeoutError as exception:
            raise errors.RequestError(f"Timed out after {self.timeout}s") from exception
        except aiohttp.ClientError as exception:
            raise errors.RequestError(str(exception)) from exception

        if retry_on_expire and path != "login" and self.is_session_expired(response):
            if await self.relogin():
                return await self.request(
                    path=path,
                    method=method,
                    params=params,
                    retry_on_expire=False
                )

        return response

    def is_session_expired(self: "pyxui.XUI", response: Response) -> bool:
        """Whether the panel answered with "you are not logged in"."""

        if response.status in REDIRECT_STATUSES:
            return "login" in response.headers.get("Location", "")

        return response.status == 401

    def verify_response(
        self: "pyxui.XUI",
        response: Response
    ) -> Union[dict, Any]:
        """Turn a panel response into a dict, raising on anything unexpected."""

        if response.status == 404:
            raise errors.NotFound()

        if response.content_type != "application/json":
            if self.is_session_expired(response):
                raise errors.NotLogin()

            raise errors.NotFound()

        try:
            result = response.json()
        except ValueError as exception:
            raise errors.BadResponse(str(exception)) from exception

        if self.raise_on_error and isinstance(result, dict) and result.get("success") is False:
            raise errors.PanelError(result.get("msg") or None)

        return result
