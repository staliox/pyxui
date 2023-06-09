import requests

import pyxui
from pyxui import errors

class Base:
    def request(
        self: "pyxui.XUI",
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
            url = f"{self.full_address}/login"
        else:
            url = f"{self.full_address}/{self.api_path}/inbounds/{path}"

        if self.session_string:
            cookie = {'session': self.session_string}
        else:
            cookie = None

        if method == "GET":
            response = requests.get(url, cookies=cookie, verify=self.https)
        elif method == "POST":
            response = requests.post(url, cookies=cookie, data=params, verify=self.https)

        return response

    def verify_response(
        self: "pyxui.XUI",
        response: requests.Response
    ) -> requests.Response:
        if response.status_code != 404 and response.headers.get('Content-Type').startswith('application/json'):
            return response.json()
        
        raise errors.NotFound()