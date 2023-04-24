from xui.methods.base import Base
from xui.methods.login import Login
from xui.methods.inbounds import Inbounds
from xui.methods.clients import Clients
class Methods(
    Base,
    Login,
    Inbounds,
    Clients
):
    pass