# SHA-CTR - crypto

### Vulnerability

Hash Length Extension attack

### Solution

Skrypt szyfruje każdy blok korzystając z `sha512(key + nonce + counter)`, nonce może być pusty, a counter jesteśmy w stanie przewidzieć

Jest biblioteka do Pythona `hashpumpy`, do której wkładamy poprzedni keystream (dostajemy go przez XOR pierwszego bloku z pierwszym blokiem `example_flag.bmp`) i nowy counter, potem wysyłając output z hashpumpa możemy przewidzieć następne keystreamy bloków:

```python
from pwn import process, log, remote
import itertools
import binascii
import hashpumpy

def xor(a: bytes, b: bytes) -> bytes:
    return bytes([(aa ^ bb) for (aa, bb) in zip(a, b)])

# r = process("python ./shactr.py", shell=True)
r = remote("shactr.ecsc25.hack.cert.pl", 5203)

r.recvuntil(b"nonce:")
r.sendline(b"")
bmp_1 = bytes.fromhex(r.recvline().decode().strip())

with open("example_flag.bmp", "rb") as f:
  example_header = f.read()[:64]

# <key> + 0000000000
ks_1 = xor(bmp_1[:64], example_header)
log.info(f"{ks_1=}")

new_hash, new_msg = hashpumpy.hashpump(
  binascii.hexlify(ks_1),
  b"0" * 10,
  b"0" * 9 + b"1",
  32,
)

r.sendlineafter(b"nonce:", binascii.hexlify(new_msg[:-10]))
bmp_2 = bytes.fromhex(r.recvline().decode().strip())

with open("recovered.bmp", "wb") as f:
  block_size = 512 // 8
  for i, block in enumerate(itertools.batched(bmp_2, block_size)):
      new_hash, new_msg = hashpumpy.hashpump(
        binascii.hexlify(ks_1),
        b"0" * 10,
        f"{i:010}".encode(),
        32,
      )
      print(new_hash)

      f.write(xor(binascii.unhexlify(new_hash), bytes(block)))
```

Flaga: `ecsc25{never_cross_the_streams}`
