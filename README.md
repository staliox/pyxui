# PyXUI 
An async python library that allows you to modify your xui panel ([alireza0 x-ui](https://github.com/alireza0/x-ui)) ([Sanaeii 3x-ui](https://github.com/MHSanaei/3x-ui)) 

> **v2.0 is async only.** Every panel method is now a coroutine and must be awaited.
> The HTTP layer moved from `requests` to `aiohttp`, and a single `ClientSession`
> is reused for the whole lifetime of the client.

## How To Install
```
pip install -U git+https://github.com/staliox/pyxui.git
```

## How To Use
- Import pyxui in your .py file
```python
import asyncio
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
    https=False, # Make note if you don't use https set False else set True
    session_string=..., # If you have session cookie to use panel without login
    timeout=10.0, # Per request timeout in seconds
    max_connections=20, # Size of the connection pool
    cache_ttl=0.0, # Seconds the inbounds list may be reused from memory, 0 disables it
    auto_relogin=True, # Login again automatically when the session expires
    raise_on_error=False, # Raise PanelError when the panel answers {"success": false}
    session=..., # Bring your own aiohttp.ClientSession, pyxui will never close it
)
```

Building the `XUI` object does not touch the network or the event loop, the
`aiohttp.ClientSession` is created on the first request.

- Always close the client when you are done, or use it as a context manager
```python
async def main():
    async with XUI(full_address="https://staliox.com:2087", panel="sanaei") as xui:
        await xui.login(USERNAME, PASSWORD)
        inbounds = await xui.get_inbounds()

asyncio.run(main())

# without the context manager
xui = XUI(full_address="https://staliox.com:2087", panel="sanaei")
try:
    ...
finally:
    await xui.close()
```

If you forget to close it, aiohttp will warn about an unclosed session on exit.

- Login in your panel
```python
from pyxui.errors import BadLogin

try:
  await xui.login(USERNAME, PASSWORD)
except BadLogin:
  ...
```

Once you have logged in, the credentials are kept in memory and the session is
refreshed automatically the first time the panel says it expired
(disable it with `auto_relogin=False`). `await xui.logout()` drops both.

- Run several calls at once
```python
inbound, stats = await asyncio.gather(
    xui.get_inbound(1),
    xui.get_client_stats(1, email="Me"),
)
```

- Get inbounds list
```python
get_inbounds = await xui.get_inbounds()

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

- Add client to the existing inbound
```python
get = await xui.add_client(
    inbound_id=1,
    email="example@gmal.com",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa",
    enable = True,
    flow = "",
    limit_ip = 0,
    total_gb = 5368709120,
    expire_time = 1684948641772, # You must pass 13 digit timestamp
    telegram_id = "",
    subscription_id = ""
)
```

- Update the existing client

Only the fields you pass are changed, the rest of the client is read from the
panel and kept as is, so a partial update is safe.
```python
get = await xui.update_client(
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

# only bump the quota, everything else stays untouched
get = await xui.update_client(inbound_id=1, email="example@gmal.com", total_gb=10737418240)
```

- Get client's information:
```python
get_client = await xui.get_client(
    inbound_id=1,
    email="Me",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa" # Make note you don't have to pass both of them (emaill, uuid), just one is enough
)

# Result
{
     'email': 'Me',
     'enable': True,
     'expiryTime': 0,
     'flow': 'xtls-rprx-vision',
     'id': '5d3d1bac-49cd-4b66-8be9-a728efa205fa',
     'limitIp': 0,
     'subId': '',
     'tgId': '',
     'totalGB': 0
}
```

- Get client's statistics:
```python
get_client = await xui.get_client_stats(
    inbound_id=1,
    email="Me",
)

# Result
{
     'id': 1,
     'inboundId': 1,
     'enable': True,
     'email': 'Me',
     'up': 111494230,
     'down': 620533614,
     'expiryTime': 0,
     'total': 0
}
```

- Delete client from the existing inbound:
```python
get_client = await xui.delete_client(
    inbound_id=1,
    email="Me",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa" # Make note you don't have to pass both of them (email, uuid), just one is enough
)
```

- Reset the traffic of a client:
```python
await xui.reset_client_traffic(
    inbound_id=1,
    email="Me"
)
```

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
vmess://eyJ2IjoiMiIsInBzIjoiU3RhbGlveC1NZSIsImFkZCI6InN0YWxpb3guY29tIiwicG9ydCI6IjQ0MyIsImlkIjoiYTg1ZGVmNTctMGE4Ni00M2QxLWIxNWMtMDQ5NDUxOTA2N2M2IiwiYWlkIjoiMCIsInNjeSI6ImF1dG8iLCJuZXQiOiJ0Y3AiLCJ0eXBlIjoid3MiLCJob3N0Ijoic3RhbGlveC5zaXRlIiwicGF0aCI6Ii8iLCJ0bHMiOiJ0bHMiLCJzbmkiOiJzdGFsaW94LnNpdGUiLCJhbHBuIjoiaDIsaHR0cC8xLjEiLCJmcCI6ImNocm9tZSJ9
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
