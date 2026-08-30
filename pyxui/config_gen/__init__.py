import json
import base64
from urllib.parse import urlencode, quote

def config_generator(protocol: str, config: dict, data: dict = None) -> str:
    """Build a vmess:// or vless:// share link out of a config dict.

    Parameters:
        protocol (``str``):
            Either ``"vmess"`` or ``"vless"``

        config (``dict``):
            The config fields, see the README for an example

        data (``dict``, optional):
            Extra query parameters, only used by vless

    Returns:
        `~str`: The share link
    """

    if protocol == "vmess":
        payload = json.dumps(config, separators=(",", ":")).encode("utf-8")

        return "vmess://" + base64.b64encode(payload).decode("utf-8")

    if protocol == "vless":
        return "vless://{}@{}:{}?{}#{}".format(
            config["id"],
            config["add"],
            config["port"],
            urlencode(data or {}),
            quote(str(config.get("ps", "")), safe="")
        )

    raise ValueError(f'Unsupported protocol "{protocol}", expected vmess or vless')
