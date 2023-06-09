from pyxui.methods import Methods

class XUI(Methods):
    def __init__(
        self,
        full_address: str,
        panel: str,
        https: bool = True,
        session_string: str = None
    ) -> None:
        super().__init__()

        self.full_address = full_address
        self.panel = panel
        self.https = https
        self.session_string = session_string
        self.api_path = None

        if self.panel == "alireza":
            self.api_path = "xui/API"
            
        elif self.panel == "sanaei":
            self.api_path = "panel/api"