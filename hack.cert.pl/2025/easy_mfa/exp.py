from flask_jwt_extended import JWTManager, create_access_token
from symbolic_mersenne_cracker.main import Untwister
import base64
import requests
from flask import Flask
from randcrack.randcrack import RandCrack
import base64


# HOST = "http://localhost:5001"
HOST = "https://easymfa.ecsc25.hack.cert.pl/"

s = requests.Session()

random_passwords = []
token = ""
for _ in range(384):
    resp = s.get(
        HOST + "/generate",
        headers={"Authorization": "Bearer " + token if token else None},
    ).json()

    print(f'"{resp["password"]}", ')
    random_passwords.append(resp["password"])
    token = resp["token"]

ut = Untwister()

guesses = []
for _ in range(8):
    guesses.append(ut.submit("?" * 32))

randoms = 8
for p in random_passwords:
    x = int.from_bytes(base64.b64decode(p), "big")
    x_1 = x >> 32
    x_2 = x & 0xFFFFFFFF

    print(x_1, x_2)

    ut.submit(bin(x_2)[2:])
    ut.submit(bin(x_1)[2:])
    randoms += 2

predictor, model = ut.get_random()

rc = RandCrack()
for i in range(624):
    rc.submit(predictor.getrandbits(32))

rc.offset(-624 - randoms)
secret = rc.predict_getrandbits(32 * 8).to_bytes(32, "big")
print("jwt secret:", secret)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = secret
jwt = JWTManager(app)
with app.test_request_context("/asdf"):
    jwt = create_access_token(identity="admin", additional_claims={"current": 1})

otp = s.post(
    HOST + "/flag",
    headers={
        "Authorization": "Bearer " + token,
    },
).text.split(" ")[-1]


def get_random_string(length):
    return predictor.getrandbits(length * 8).to_bytes(length, "big")


def get_mfa():
    return get_random_string(8)


print("leaked otp:", otp[:-5])

while get_mfa() != base64.b64decode(otp[:-5]):
    continue

for _ in range(200):
    pred_token = base64.b64encode(get_mfa()).decode()
    print("testing token", pred_token)

    resp = s.post(
        HOST + "/flag",
        headers={"Authorization": "Bearer " + jwt},
        json={"OTP": pred_token},
    ).text
    print(resp)
    if "ecsc25" in resp:
        break
