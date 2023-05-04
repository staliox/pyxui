from pyxui.methods.base import Base
from pyxui.methods.login import Login
from pyxui.methods.inbounds import Inbounds
from pyxui.methods.clients import Clients

class Methods(
    Base,
    Login,
    Inbounds,
    Clients
):
    pass
