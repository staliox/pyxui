import json
from typing import Union

import pyxui
from pyxui import errors

def _build_settings(client: dict) -> str:
    """Serialize a single client into the inbound settings payload."""

    return json.dumps({
        "clients": [client],
        "decryption": "none",
        "fallbacks": []
    })

class Clients:
    async def get_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = None,
        uuid: str = None
    ) -> Union[dict, errors.NotFound]:
        """Get client from the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id

            email (``str``, optional):
               Email of the client

            uuid (``str``, optional):
               UUID of the client

        Returns:
            `~Dict`: On success, a dict is returned or else 404 an error will be raised
        """

        if not email and not uuid:
            raise ValueError("Either email or uuid must be given")

        inbound = await self.find_inbound(inbound_id)

        try:
            settings = json.loads(inbound.get("settings") or "{}")
        except ValueError as exception:
            raise errors.BadResponse(str(exception)) from exception

        for client in settings.get("clients") or []:
            if (email and client.get("email") == email) or (uuid and client.get("id") == uuid):
                return client

        raise errors.NotFound()

    async def get_client_stats(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str,
    ) -> Union[dict, errors.NotFound]:
        """Get client stats from the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id

            email (``str``):
               Email of the client

        Returns:
            `~Dict`: On success, a dict is returned or else 404 error will be raised
        """

        if not email:
            raise ValueError("email must be given")

        if self.panel == "sanaei":
            try:
                response = await self.request(
                    path=f"getClientTraffics/{email}",
                    method="GET"
                )

                result = self.verify_response(response)

                if isinstance(result, dict) and result.get("obj"):
                    return result["obj"]
            except (errors.NotFound, errors.PanelError):
                pass

        inbound = await self.find_inbound(inbound_id)

        for client in inbound.get("clientStats") or []:
            if client.get("email") == email:
                return client

        raise errors.NotFound()

    async def add_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str,
        uuid: str,
        enable: bool = True,
        flow: str = "",
        limit_ip: int = 0,
        total_gb: int = 0,
        expire_time: int = 0,
        telegram_id: str = "",
        subscription_id: str = "",
    ) -> Union[dict, errors.NotFound]:
        """Add client to the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id

            email (``str``):
               Email of the client

            uuid (``str``):
               UUID of the client

            enable (``bool``, optional):
               Status of the client

            flow (``str``, optional):
               Flow of the client

            limit_ip (``int``, optional):
               IP Limit of the client

            total_gb (``int``, optional):
                Download and upload limitation of the client, in bytes

            expire_time (``int``, optional):
                Client expiration date, in timestamp (epoch)

            telegram_id (``str``, optional):
               Telegram id of the client

            subscription_id (``str``, optional):
               Subscription id of the client

        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """

        params = {
            "id": inbound_id,
            "settings": _build_settings({
                "id": uuid,
                "email": email,
                "enable": enable,
                "flow": flow,
                "limitIp": limit_ip,
                "totalGB": total_gb,
                "expiryTime": expire_time,
                "tgId": telegram_id,
                "subId": subscription_id
            })
        }

        response = await self.request(
            path="addClient",
            method="POST",
            params=params
        )

        self.clear_cache()

        return self.verify_response(response)

    async def delete_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = None,
        uuid: str = None
    ) -> Union[dict, errors.NotFound]:
        """Delete client from the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id

            email (``str``, optional):
               Email of the client

            uuid (``str``, optional):
               UUID of the client

        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """

        find_client = await self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid
        )

        response = await self.request(
            path=f"{inbound_id}/delClient/{find_client['id']}",
            method="POST"
        )

        self.clear_cache()

        return self.verify_response(response)

    async def update_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = None,
        uuid: str = None,
        enable: bool = None,
        flow: str = None,
        limit_ip: int = None,
        total_gb: int = None,
        expire_time: int = None,
        telegram_id: str = None,
        subscription_id: str = None,
    ) -> Union[dict, errors.NotFound]:
        """Update an existing client.

        Only the given fields are changed, everything else keeps its current
        value, so a partial update never wipes the rest of the client.

        Parameters:
            inbound_id (``int``):
                Inbound id

            email (``str``, optional):
               Email of the client, used to look it up

            uuid (``str``, optional):
               UUID of the client, used to look it up

            enable (``bool``, optional):
               Status of the client

            flow (``str``, optional):
               Flow of the client

            limit_ip (``int``, optional):
               IP Limit of the client

            total_gb (``int``, optional):
                Download and upload limitation of the client, in bytes

            expire_time (``int``, optional):
                Client expiration date, in timestamp (epoch)

            telegram_id (``str``, optional):
               Telegram id of the client

            subscription_id (``str``, optional):
               Subscription id of the client

        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """

        find_client = await self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid
        )

        updates = {
            "id": uuid,
            "email": email,
            "enable": enable,
            "flow": flow,
            "limitIp": limit_ip,
            "totalGB": total_gb,
            "expiryTime": expire_time,
            "tgId": telegram_id,
            "subId": subscription_id
        }

        client = dict(find_client)
        client.update({key: value for key, value in updates.items() if value is not None})

        params = {
            "id": inbound_id,
            "settings": _build_settings(client)
        }

        response = await self.request(
            path=f"updateClient/{find_client['id']}",
            method="POST",
            params=params
        )

        self.clear_cache()

        return self.verify_response(response)

    async def reset_client_traffic(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = None,
        uuid: str = None
    ) -> Union[dict, errors.NotFound]:
        """Reset the traffic of a client in the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id

            email (``str``, optional):
               Email of the client

            uuid (``str``, optional):
               UUID of the client

        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """

        find_client = await self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid
        )

        response = await self.request(
            path=f"{inbound_id}/resetClientTraffic/{find_client['email']}",
            method="POST"
        )

        self.clear_cache()

        return self.verify_response(response)
