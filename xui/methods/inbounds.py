import xui
from xui import errors

class Inbounds:
    def get_inbounds(self: "xui.XUI") -> dict:
        _send_request = self.request("list")

        if _send_request.status_code == 404:
            raise errors.NotFound()

        return _send_request.json()