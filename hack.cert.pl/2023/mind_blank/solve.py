import asyncio
from concurrent.futures import ThreadPoolExecutor
import itertools
import socket
from threading import Lock
from server import LFSR, long_to_bytes

HOST = "mind-blank.ecsc23.hack.cert.pl"
PORT = 5001

DIFFICULTY = 48  # 48
number_of_workers = 25
bits = []
lock = Lock()

gdate = None


def socket_handler(id: str):
    global gdate
    global bits
    ret = None

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    date = s.recv(1024)
    print(f"socket({id}): date={date}")
    lock.acquire()
    print(f"socket({id}): acquired the lock")

    if gdate is None:
        gdate = date

    assert gdate == date

    for x in bits:
        s.send(f"{x}\n".encode())
        ret = s.recv(1024)

    for _ in range(DIFFICULTY - len(bits)):
        s.send("1\n".encode())
        ret = s.recv(1024)

        if ret.startswith(b"Correct"):
            bits.append(1)
            print(f"socket({id}): 1, bits:", bits)
        elif ret.startswith(b"Nope"):
            bits.append(0)
            print(f"socket({id}): 0, bits:", bits)
            break

    s.close()
    lock.release()

    if len(bits) == DIFFICULTY and bits[-1] != 0:
        flag = ret.split()[1]
        return flag


async def main():
    global bits

    loop = asyncio.get_running_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=40))

    # bits = [0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1]
    # results = [b"52b3dc89bb383c553bc023273d84e5dfee7112c850ad4c7f8514ccfaf7222096a662a930caf0b34a2ef4147eeaa961ec9b"]
    results = await asyncio.gather(
        *[asyncio.to_thread(socket_handler, i) for i in range(number_of_workers)],
    )

    flag = next((f for f in results if f is not None), None)
    if not flag:
        exit(1)

    print("encrypted flag:", flag)
    flag = bytes.fromhex(flag.decode())

    state = bits[:21]

    taps = []
    for x in itertools.combinations(range(20), r=10):
        lfsr = LFSR(list(x), 1)
        lfsr.state = state

        if [lfsr.next_bit() for _ in range(48)] == bits:
            taps = list(x)
            print("bruted taps:", taps)
            break

    lfsr = LFSR(taps, 1)
    lfsr.state = state
    for _ in range(48):
        lfsr.next_bit()

    bits = [lfsr.next_bit() for _ in range(len(flag) * 8)]
    keystream = long_to_bytes(int("".join([str(b) for b in bits]), 2))
    ciphertext = bytes([c ^ k for c, k in zip(flag, keystream)])
    print(ciphertext)


if __name__ == "__main__":
    asyncio.run(main())
