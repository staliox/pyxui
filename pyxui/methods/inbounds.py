from typing import Union

import xui
from xui import errors

class Inbounds:
    def get_inbounds(
        self: "xui.XUI"
    ) -> Union[dict, errors.NotFound]:
        """Get inbounds of xui panel.
        
        Returns:
            `~Dict | errors.NotFound`: On success, a dict is returned else 404 error will be raised
        """
        
        send_request = self.request(
            path="list",
            method="GET"
        )

<<<<<<< HEAD
        if send_request.status_code != 404 and send_request.headers.get('Content-Type').startswith('application/json'):
            return send_request.json()
        else:
            raise errors.NotFound()
        
    def get_inbound(
        self: "xui.XUI",
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
=======
        if _send_request.status_code != 404 and _send_request.headers.get('Content-Type').startswith('application/json'):
            return _send_request.json()
        else:
            raise errors.NotFound()
>>>>>>> 3c5a0c91d28d9de6b5919a3391055ae670ccfbe7
