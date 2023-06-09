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
        
        
        if self.panel == "alireza":
            path = ""
            
        elif self.panel == "sanaei":
            path = "list"
        
        response = self.request(
            path=path,
            method="GET"
        )

        return self.verify_response(response)
        
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
        
        response = self.request(
            path=f"get/{inbound_id}",
            method="GET"
        )

        return self.verify_response(response)