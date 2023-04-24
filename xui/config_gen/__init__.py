import json
import base64
from urllib.parse import urlencode

def config_generator(protocol: str, config = dict, data: dict = None) -> str:
    if protocol == "vmess":
        string = "vmess://" + base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')

    elif protocol == "vless":
        string = "vless://{}@{}:{}?{}#{}".format(config['id'], config['add'], config['port'], urlencode(data), config['ps'])

    return string