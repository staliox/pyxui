from typing import Union

import pyxui
from pyxui import errors

class Inbounds:
    def get_inbounds(
        self: "pyxui.XUI"
    ) -> Union[dict, errors.NotFound]:
        """Get inbounds of xui panel.
        
        Returns:
            `~Dict | errors.NotFound`: On success, a dict is returned else 404 error will be raised
        """
        
        send_request = self.request(
            path="list",
            method="GET"
        )

        if send_request.status_code != 404 and send_request.headers.get('Content-Type').startswith('application/json'):
            return send_request.json()
        else:
            raise errors.NotFound()
        
    def get_inbound(
        self: "pyxui.XUI",
        inbound_id: int
    ) -> Union[dict, errors.NotFound]:
        """Get inbounds of xui panel.

        Parameters:
            inbound_id (``int``):
                Inbound id
        
        Returns:
            `~Dict | errors.NotFound`: On success, a dict is returned else 404 error will be raised
        """
        
        send_request = self.request(
            path=f"get/{inbound_id}",
            method="GET"
        )

        if send_request.status_code != 404 and send_request.headers.get('Content-Type').startswith('application/json'):
            return send_request.json()
        else:
            raise errors.NotFound()
