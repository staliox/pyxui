import json
from typing import Union

import pyxui
from pyxui import errors

class Clients:
    def get_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = False,
        uuid: str = False
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
        
        get_inbounds = self.get_inbounds()
        
        if not email and not uuid:
            raise ValueError()
        
        for inbound in get_inbounds['obj']:
            if inbound['id'] != inbound_id:
                continue
            
            settings = json.loads(inbound['settings'])
            
            for client in settings['clients']:
                if client['email'] != email and client['id'] != uuid:
                    continue
                
                return client

        raise errors.NotFound()

    def get_client_stats(
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
        
        get_inbounds = self.get_inbounds()
        
        if not email:
            raise ValueError()
        
        for inbound in get_inbounds['obj']:
            if inbound['id'] != inbound_id:
                continue
            
            client_stats = inbound['clientStats']
            
            for client in client_stats:
                if client['email'] != email:
                    continue
                
                return client

        raise errors.NotFound()

    def add_client(
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
                
            limit_ip (``str``, optional):
               IP Limit of the client
                
            total_gb (``str``, optional):
                Download and uploader limition of the client and it's in bytes
                
            expire_time (``str``, optional):
                Client expiration date and it's in timestamp (epoch)
                
            telegram_id (``str``, optional):
               Telegram id of the client
                
            subscription_id (``str``, optional):
               Subscription id of the client
            
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
            ],
            "decryption": "none",
            "fallbacks": []
        }
        
        params = {
            "id": inbound_id,
            "settings": json.dumps(settings)
        }

        response = self.request(
            path="addClient",
            method="POST",
            params=params
        )

        return self.verify_response(response)

    def delete_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = False,
        uuid: str = False
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
        
        find_client = self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid
        )
        
        response = self.request(
            path=f"{inbound_id}/delClient/{find_client['id']}",
            method="POST"
        )

        return self.verify_response(response)

    def update_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str,
        uuid: str,
        enable: bool,
        flow: str,
        limit_ip: int,
        total_gb: int,
        expire_time: int,
        telegram_id: str,
        subscription_id: str,
    ) -> Union[dict, errors.NotFound]:
        """Add client to the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``):
               Email of the client
                
            uuid (``str``):
               UUID of the client
                
            enable (``bool``):
               Status of the client
                
            flow (``str``):
               Flow of the client
                
            limit_ip (``str``):
               IP Limit of the client
                
            total_gb (``str``):
                Download and uploader limition of the client and it's in bytes
                
            expire_time (``str``):
                Client expiration date and it's in timestamp (epoch)
                
            telegram_id (``str``):
               Telegram id of the client
                
            subscription_id (``str``):
               Subscription id of the client
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        
        find_client = self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid
        )
        
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
            ],
            "decryption": "none",
            "fallbacks": []
        }
            
        params = {
            "id": inbound_id,
            "settings": json.dumps(settings)
        }
        
        response = self.request(
            path=f"updateClient/{find_client['id']}",
            method="POST",
            params=params
        )

        return self.verify_response(response)