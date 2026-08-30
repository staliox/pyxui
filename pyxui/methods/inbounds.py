import time
from typing import Union

import pyxui
from pyxui import errors

class Inbounds:
    def clear_cache(self: "pyxui.XUI") -> None:
        """Drop the cached inbounds list."""

        self._inbounds_cache = None
        self._inbounds_cache_at = 0.0

    async def get_inbounds(
        self: "pyxui.XUI",
        use_cache: bool = True
    ) -> Union[dict, errors.NotFound]:
        """Get inbounds of the xui panel.

        Parameters:
            use_cache (``bool``, optional):
                Reuse the previous result while it's younger than ``cache_ttl``

        Returns:
            `~Dict | errors.NotFound`: On success, a dict is returned else 404 error will be raised
        """

        if use_cache and self.cache_ttl > 0 and self._inbounds_cache is not None:
            if (time.monotonic() - self._inbounds_cache_at) < self.cache_ttl:
                return self._inbounds_cache

        path = "" if self.panel == "alireza" else "list"

        response = await self.request(
            path=path,
            method="GET"
        )

        result = self.verify_response(response)

        if self.cache_ttl > 0:
            self._inbounds_cache = result
            self._inbounds_cache_at = time.monotonic()

        return result

    async def get_inbound(
        self: "pyxui.XUI",
        inbound_id: int
    ) -> Union[dict, errors.NotFound]:
        """Get a single inbound of the xui panel.

        Parameters:
            inbound_id (``int``):
                Inbound id

        Returns:
            `~Dict | errors.NotFound`: On success, a dict is returned else 404 error will be raised
        """

        response = await self.request(
            path=f"get/{inbound_id}",
            method="GET"
        )

        return self.verify_response(response)

    async def find_inbound(
        self: "pyxui.XUI",
        inbound_id: int
    ) -> dict:
        """Return the raw object of a single inbound.

        Tries the dedicated endpoint first (one small response) and falls back
        to filtering the full list for panels that don't expose it.

        Parameters:
            inbound_id (``int``):
                Inbound id

        Returns:
            `~Dict`: On success, the inbound object is returned else 404 error will be raised
        """

        if self._single_inbound_supported is not False:
            try:
                result = await self.get_inbound(inbound_id)

                if isinstance(result, dict) and result.get("obj"):
                    self._single_inbound_supported = True

                    return result["obj"]
            except (errors.NotFound, errors.PanelError):
                self._single_inbound_supported = False

        inbounds = await self.get_inbounds()

        for inbound in inbounds.get("obj") or []:
            if inbound.get("id") == inbound_id:
                return inbound

        raise errors.NotFound(f"Inbound {inbound_id} does not exist")
