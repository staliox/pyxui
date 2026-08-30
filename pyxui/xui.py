import asyncio
import aiohttp
from typing import Optional, Tuple

from pyxui import errors
from pyxui.methods import Methods

#: panel name -> (api path, session cookie name)
PANELS = {
    "alireza": ("xui/API", "x-ui"),
    "sanaei": ("panel/api", "3x-ui"),
}

class XUI(Methods):
    """Asynchronous client for the x-ui / 3x-ui panel API.

    A single ``aiohttp.ClientSession`` is kept alive for the whole lifetime of
    the instance, so connections (and the TLS handshake) are reused between
    calls. The session is created lazily on the first request because aiohttp
    requires a running event loop to build one.

    Parameters:
        full_address (``str``):
            Base address of the panel, e.g. ``https://example.com:2087``.
            A base path is allowed too, e.g. ``https://example.com:2087/secret``

        panel (``str``):
            Panel name, either ``"alireza"`` or ``"sanaei"``

        https (``bool``, optional):
            Whether the TLS certificate of the panel should be verified.
            Kept for backward compatibility, prefer ``verify_ssl``.

        session_string (``str``, optional):
            An already known session cookie, lets you skip ``login()``

        timeout (``float``, optional):
            Per request timeout in seconds

        max_connections (``int``, optional):
            Size of the underlying connection pool

        cache_ttl (``float``, optional):
            How long (seconds) the inbounds list may be reused from memory.
            ``0`` disables the cache.

        auto_relogin (``bool``, optional):
            Re-login automatically once when the session expires, the
            credentials given to ``login()`` are reused.

        raise_on_error (``bool``, optional):
            Raise `~pyxui.errors.PanelError` when the panel answers with
            ``{"success": false}`` instead of returning the raw payload.

        session (`~aiohttp.ClientSession`, optional):
            Bring your own session. pyxui will use it as is and will never
            close it, that stays your responsibility.
    """

    def __init__(
        self,
        full_address: str,
        panel: str,
        https: bool = True,
        session_string: str = None,
        timeout: float = 10.0,
        max_connections: int = 20,
        verify_ssl: bool = None,
        cache_ttl: float = 0.0,
        auto_relogin: bool = True,
        raise_on_error: bool = False,
        session: aiohttp.ClientSession = None,
    ) -> None:
        super().__init__()

        if panel not in PANELS:
            raise errors.UnsupportedPanel(
                f'Unknown panel "{panel}", expected one of {", ".join(PANELS)}'
            )

        self.full_address = full_address.rstrip("/")
        self.panel = panel
        self.https = https
        self.session_string = session_string
        self.api_path, self.cookie_name = PANELS[panel]

        self.timeout = timeout
        self.max_connections = max_connections
        self.verify_ssl = https if verify_ssl is None else verify_ssl
        self.cache_ttl = cache_ttl
        self.auto_relogin = auto_relogin
        self.raise_on_error = raise_on_error

        self._session: Optional[aiohttp.ClientSession] = session
        self._owns_session = session is None
        self._session_lock = asyncio.Lock()
        self._login_lock = asyncio.Lock()
        self._credentials: Optional[Tuple[str, str, Optional[str]]] = None
        self._inbounds_cache: Optional[dict] = None
        self._inbounds_cache_at: float = 0.0
        
        self._single_inbound_supported: Optional[bool] = None

    async def __aenter__(self) -> "XUI":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def close(self) -> None:
        if self._session is None or not self._owns_session:
            return

        if not self._session.closed:
            await self._session.close()

        self._session = None
