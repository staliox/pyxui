import requests
from typing import Union

import xui

class Base:
    @property
    def _panel_address(self: "xui.XUI") -> str:
        return f"{self.https}://{self.address}:{self.port}{self.path}/"

    def request(self: "xui.XUI", query: str, params: Union[dict, bool] = False) -> requests.Response:
        if query == "login":
            url = self._panel_address + query
        else:
            url = self._panel_address + "xui/API/inbounds/" + query

        if self.session_string:
            cookie = {'session': self.session_string}
        else:
            cookie = None

        if not params:
            response = requests.get(url, cookies=cookie)
        else:
            response = requests.post(url, cookies=cookie, data=params)

        return response