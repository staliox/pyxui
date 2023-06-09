# PyXUI 
An application with python that allows you to modify your xui panel ([alireza0 x-ui](https://github.com/alireza0/x-ui)) ([Sanaeii 3x-ui](https://github.com/MHSanaei/3x-ui)) 

## How To Install
```
pip install pyxui
```

## How To Use
- Import pyxui in your .py file
```python
from pyxui import XUI

# Basic:
xui = XUI(
    full_address="https://staliox.com:2087",
    panel="alireza", # Your panel name, "alireza" or "sanaei"
)

# Advanced:
xui = XUI(
    full_address="http://staliox.site:2087",
    panel="alireza", # Your panel name, "alireza" or "sanaei"
    https=False # Make note if you don't use https set False else set True
    session_string=... # If you have session cookie to use panel without login
)
```

- Login in your panel
```python
from pyxui.errors import BadLogin

try:
  xui.login(USERNAME, PASSWORD)
except BadLogin:
  ...
```

- Get inbounds list
```python
get_inbounds = xui.get_inbounds()

# Result
{
    "success": true,
    "msg": "",
    "obj": [
        {
            "id": 1,
            "up": 552345026,
            "down": 18164200325,
            "total": 0,
            "remark": "Staliox",
            "enable": true,
            "expiryTime": 0,
            "clientStats": [
                {
                    "id": 1,
                    "inboundId": 1,
                    "enable": true,
                    "email": "Me",
                    "up": 191308877,
                    "down": 4945030148,
                    "expiryTime": 0,
                    "total": 0
                }
            ],
            "listen": "",
            "port": 443,
            "protocol": "vless",
            "settings": "{\n  \"clients\": [\n    {\n      \"email\": \"Me\",\n      \"enable\": true,\n      \"expiryTime\": 0,\n      \"flow\": \"\",\n      \"id\": \"c6419651-68d7-gfhg-d611-32v5df41g105\",\n      \"limitIp\": 0,\n      \"subId\": \"\",\n      \"tgId\": \"@staliox\",\n      \"totalGB\": 0\n    }\n  ],\n  \"decryption\": \"none\",\n  \"fallbacks\": []\n}",
            "tag": "inbound-443",
            "sniffing": "{\n  \"enabled\": true,\n  \"destOverride\": [\n    \"http\",\n    \"tls\"\n  ]\n}"
        }
    ]
}
```

- Add client to exist inbound
```python
get = xui.add_client(
    inbound_id=1,
    email="example@gmal.com",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa",
    enable = True,
    flow = "",
    limit_ip = 0,
    total_gb = 5368709120,
    expire_time = 1684948641772,
    telegram_id = "",
    subscription_id = ""
)
```

- Update exist client
```python
get = xui.update_client(
    inbound_id=1,
    email="example@gmal.com",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa",
    enable = True,
    flow = "",
    limit_ip = 0,
    total_gb = 5368709120,
    expire_time = 1684948641772,
    telegram_id = "",
    subscription_id = ""
)
```

- Get client information:
```python
get_client = xui.get_client(
    inbound_id=1,
    email="Me",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa" # Make note you don't have to pass both of them (emaill, uuid), just one is enough
)

# Result
{
    'id': 1,
    'inboundId': 1,
    'enable': True,
    'email': 'Me',
    'up': 194895832,
    'down': 4959786483,
    'expiryTime': 0,
    'total': 0
}
```

- Delete client from exist inbound:
```python
get_client = xui.delete_client(
    inbound_id=1,
    email="Me",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa" # Make note you don't have to pass both of them (email, uuid), just one is enough
)

# Create vmess and vless config string
- Import config_generator
```python
from pyxui.config_gen import config_generator
```

- VMESS:
```python
config = {
    "v": "2",
    "ps": "Staliox-Me",
    "add": "staliox.com",
    "port": "443",
    "id": "a85def57-0a86-43d1-b15c-0494519067c6",
    "aid": "0",
    "scy": "auto",
    "net": "tcp",
    "type": "ws",
    "host": "staliox.site",
    "path": "/",
    "tls": "tls",
    "sni": "staliox.site",
    "alpn": "h2,http/1.1",
    "fp": "chrome"
}

generate_config = config_generator("vmess", config)

# Result
vmess://eyJ2IjogIjIiLCAicHMiOiAiU3RhbGlveC1NZSIsICJhZGQiOiAic3RhbGlveC5jb20iLCAicG9ydCI6ICI0NDMiLCAiaWQiOiAiYTg1ZGVmNTctMGE4Ni00M2QxLWIxNWMtMDQ5NDUxOTA2N2M2IiwgImFpZCI6ICIwIiwgInNjeSI6ICJhdXRvIiwgIm5ldCI6ICJ0Y3AiLCAidHlwZSI6ICJ3cyIsICJob3N0IjogInN0YWxpb3guc2l0ZSIsICJwYXRoIjogIi8iLCAidGxzIjogInRscyIsICJzbmkiOiAic3RhbGlveC5zaXRlIiwgImFscG4iOiAiaDIsaHR0cC8xLjEiLCAiZnAiOiAiY2hyb21lIn0=
```

- VLESS:
```python
config = {
    "ps": "Staliox-Me",
    "add": "staliox.com",
    "port": "443",
    "id": "a85def57-0a86-43d1-b15c-0494519067c6"
}

data = {
    "security": "tls",
    "type": "ws",
    "host": "staliox.site",
    "path": "/",
    "sni": "staliox.site",
    "alpn": "h2,http/1.1",
    "fp": "chrome"
}

generate_config = config_generator("vless", config, data)

# Result
vless://a85def57-0a86-43d1-b15c-0494519067c6@staliox.com:443?security=tls&type=ws&host=staliox.site&path=%2F&tls=tls&sni=staliox.site&alpn=h2%2Chttp%2F1.1&fp=chrome#Staliox-Me
```
