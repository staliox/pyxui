from typing import Any

import xui

class Clients:
    def get_client(self: "xui.XUI", id: int, email: str) -> Any:
        get_inbounds = self.get_inbounds()

        for inbound in get_inbounds['obj']:
            if inbound['id'] != id:
                continue

            for client in inbound['clientStats']:
                if client['email'] != email:
                    continue

                return client

    def add_client(self: "xui.XUI", id: int, email: str, uuid: str, limit_ip: int, expire_time: int) -> Any:
        params = {
            "id": id,
            "settings": '{{\n  "clients": [\n    {{\n      "id": "{0}",\n      "email": "{1}",\n      "limitIp": {2},\n      "expiryTime": {3}\n    }}\n  ]}}'.format(uuid, email, limit_ip, expire_time)
        }

        _send_request = self.request("addClient", params)
        return _send_request.json()