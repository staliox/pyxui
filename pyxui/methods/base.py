import requests

import xui

class Base:
    @property
    def _panel_address(self: "xui.XUI") -> str:
        return f"{self.https}://{self.address}:{self.port}{self.path}/"

<<<<<<< HEAD
    def request(
        self: "xui.XUI",
        path: str,
        method: str,
        params: dict = None
    ) -> requests.Response:
        """Request to xui panel.

        Parameters:
            path (``str``):
                Your request path, you can see all of them in https://github.com/alireza0/x-ui#api-routes
                
            method (``str``):
                Your request method, GET or POST
                
            params (``dict``, optional):
                Your request parameters, None is set for default but it's necessary for some POST methods

        Returns:
            `~requests.Response`: On success, the response is returned.
        """
        
        if path == "login":
            url = self._panel_address + path
=======
    def request(self: "xui.XUI", query: str, params: Union[dict, bool] = None) -> requests.Response:
        if query == "login":
            url = self._panel_address + query
>>>>>>> 3c5a0c91d28d9de6b5919a3391055ae670ccfbe7
        else:
            url = self._panel_address + "xui/API/inbounds/" + path

        if self.session_string:
            cookie = {'session': self.session_string}
        else:
            cookie = None

<<<<<<< HEAD
        if method == "GET":
            response = requests.get(url, cookies=cookie, verify=False)
        elif method == "POST":
            response = requests.post(url, cookies=cookie, data=params, verify=False)
=======
        if not params:
            response = requests.get(url, cookies=cookie)
        else:
            response = requests.post(url, cookies=cookie, data=params)
>>>>>>> 3c5a0c91d28d9de6b5919a3391055ae670ccfbe7

        return response
