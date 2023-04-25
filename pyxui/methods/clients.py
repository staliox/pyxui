import json
from typing import Union

import xui
from xui import errors

class Clients:
    def get_client(
        self: "xui.XUI",
        inbound_id: int,
        email: str = False,
        uuid: str = False
    ) -> Union[dict, errors.NotFound]:
        """Get client from exist inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``, optional):
               Email of client
                
            uuid (``str``, optional):
               UUID of client
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        
        get_inbounds = self.get_inbounds()
        
        if not email and not uuid:
            raise ValueError()
        
        for inbound in get_inbounds['obj']:
            if inbound['id'] != inbound_id:
                continue
            
            settings = json.loads(inbound['settings'])
            print(json.dumps(settings))
            
            for client in settings['clients']:
                if client['email'] != email and client['id'] != uuid:
                    continue
                
                return client

<<<<<<< HEAD
        raise errors.NotFound()

    def add_client(
        self: "xui.XUI",
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
        """Add client to exist inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``):
               Email of client
                
            enable (``bool``, optional):
               Status of client
                
            flow (``str``, optional):
               Flow of client
                
            uuid (``str``, optional):
               UUID of client
                
            limit_ip (``str``, optional):
               IP Limit of client
                
            total_gb (``str``, optional):
                Download and uploader limition of client and it's in bytes
                
            expire_time (``str``, optional):
                Client expiration date and it's in timestamp (epoch)
                
            telegram_id (``str``, optional):
               Telegram id of client
                
            subscription_id (``str``, optional):
               Subscription id of client
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        
        settings = {
            "clients": [
                {
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
            ]
        }
        
        params = {
            "id": inbound_id,
            "settings": json.dumps(settings)
        }

        send_request = self.request(
            path="addClient",
            method="POST",
            params=params
        )

        if send_request.status_code != 404 and send_request.headers.get('Content-Type').startswith('application/json'):
            return send_request.json()
        else:
            raise errors.NotFound()

    def delete_client(
        self: "xui.XUI",
        inbound_id: int,
        email: str = False,
        uuid: str = False
    ) -> Union[dict, errors.NotFound]:
        """Delete client from exist inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``, optional):
               Email of client
                
            uuid (``str``, optional):
               UUID of client
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        
        find_client = self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid
        )
        
        send_request = self.request(
            path=f"{inbound_id}/delClient/{find_client['uuid']}",
            method="POST"
        )

        if send_request.status_code != 404 and send_request.headers.get('Content-Type').startswith('application/json'):
            return send_request.json()
        else:
            raise errors.NotFound()
=======
    def add_client(self: "xui.XUI", inbound_id: int, email: str, uuid: str, limit_ip: int, total_gb: int, expire_time: int) -> Any:
        params = {
            "id": inbound_id,
            "settings": '{{\n  "clients": [\n    {{\n      "id": "{}",\n      "email": "{}",\n      "limitIp": {},\n      "totalGB": {},\n      "expiryTime": {}\n    }}\n  ]}}'.format(uuid, email, limit_ip, total_gb, expire_time)
        }

        _send_request = self.request("addClient", params)

        if _send_request.status_code != 404 and _send_request.headers.get('Content-Type').startswith('application/json'):
            return _send_request.json()
        else:
            raise errors.NotFound()
>>>>>>> 3c5a0c91d28d9de6b5919a3391055ae670ccfbe7
