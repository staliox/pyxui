import xui
from xui import errors

class Inbounds:
    def get_inbounds(self: "xui.XUI") -> dict:
        _send_request = self.request("list")

        if _send_request.status_code != 404 and _send_request.headers.get('Content-Type').startswith('application/json'):
            return _send_request.json()
        else:
            raise errors.NotFound()