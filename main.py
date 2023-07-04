from pyxui import XUI

xui = XUI("http://5.42.83.171:2034", "sanaei", False)
xui.login("mazdak", "m13851385")

print(xui.get_client_stats(inbound_id=3, email="Farzad"))
