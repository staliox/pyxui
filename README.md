# PyXUI
An application with python that allows you to modify your xui panel ([Sanaeii 3x-ui](https://github.com/MHSanaei/3x-ui))

## How To Use
- Download repositiory and extract it
- Import xui in your .py file
```python
from xui import XUI

xui = XUI("staliox.com, 54321, True) # Make note if you use https set True else don't set anything
xui = XUI("staliox.com, 54321, True, "6fo3") # If you set panel path, you can set your panel path string
```

- Login in your panel
```python
from xui.errors import BadLogin

try:
  xui.login(USERNAME, PASSWORD)
except BadLogin:
  ...
```

- Get inbounds list
```python
get_inbounds = xui.get_inbounds()

# Result:
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

- Add client to inbound
```python
get = xui.add_client(
    inbound_id=1,
    email="fdsfgf@gmal.com",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa",
    limit_ip=0,
    total_gb=5368709120,
    expire_time=1684948641772
)
```

- Get client information:
```python
get_client = xui.get_client(
    id=1,
    email="Me"
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
