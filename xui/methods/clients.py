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
