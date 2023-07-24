import os

from Crypto.Util.number import getPrime, bytes_to_long


def pad(data, bitsize):
    missing = (bitsize - len(data) * 8) // 8
    return os.urandom(missing // 2) + data + os.urandom(missing // 2)


def main():
    p = getPrime(1024)
    q = getPrime(1024)
    N = p * q
    e1 = getPrime(32)
    e2 = getPrime(32)
    assert p != q
    assert e1 != e2

    m = bytes_to_long(pad(open("flag.txt", 'rb').read(), 2047))
    c1 = pow(m, e1, N)
    c2 = pow(m, e2, N)
    print(f'N = {N}')
    print(f'e1 = {e1}')
    print(f'e2 = {e2}')
    print(f'c1 = {c1}')
    print(f'c2 = {c2}')


main()
