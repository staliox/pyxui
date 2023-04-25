from pyxui.methods import Methods

class XUI(Methods):
    def __init__(
        self,
        address: str,
        port: int,
        https: bool = False,
        path: str = False,
        session_string: str = None
    ) -> None:
        super().__init__()

        self.address = address
        self.port = port
        self.https = "https" if https else "http"
        self.path = "" if not path else f"/{path}"
        self.session_string = session_string
