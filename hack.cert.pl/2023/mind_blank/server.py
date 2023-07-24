import binascii
import time

import hmac
import random
from typing import List


def chunk(input_data, size):
    assert len(input_data) % size == 0, \
        "can't split data into chunks of equal size, try using chunk_with_remainder or pad data"
    return [input_data[i:i + size] for i in range(0, len(input_data), size)]


def long_to_bytes(data):
    if data == 0:
        return "\0"
    data = int(data)
    data = hex(data).rstrip('L').lstrip('0x')
    if len(data) % 2 == 1:
        data = '0' + data
    return bytes(bytearray(int(c, 16) for c in chunk(data, 2)))


def long_to_bits(n: int) -> List[int]:
    return [n >> i & 1 for i in range(0, n.bit_length())]


class LFSR:
    def __init__(self, taps, seed):
        self.state = long_to_bits(seed)
        self.taps = taps

    def _new_bit(self):
        b = 0
        for t in self.taps:
            b = b ^ self.state[t]
        return b

    def next_bit(self):
        ret = self.state[0]
        self.state = self.state[1:] + [self._new_bit()]
        return ret


def main():
    difficulty = 48
    ts = time.ctime(time.time())
    print(f"{ts} can you read my mind?")
    random.seed(hmac.digest(b'SOME_SECRET_YOU_DONT_HAVE', str("Sat Jul 22 14:01:05 2023").encode(), digest='sha256'))
    taps = random.sample(range(20), k=10)
    seed = random.randint(2 ** 20, 2 ** 21)
    lfsr = LFSR(taps, seed)
    bits = [lfsr.next_bit() for _ in range(difficulty)]
    print(bits)
    for bit in bits:
        guess = int(input(">"))
        if guess == bit:
            print("Correct!")
        else:
            print("Nope!")
            return
    flag = open("flag.txt", 'rb').read()
    bits = [lfsr.next_bit() for _ in range(len(flag) * 8)]
    keystream = long_to_bytes(int(''.join([str(b) for b in bits]), 2))
    ciphertext = bytes([c ^ k for c, k in zip(flag, keystream)])
    print(binascii.hexlify(ciphertext).decode())


if __name__ == '__main__':
    main()
