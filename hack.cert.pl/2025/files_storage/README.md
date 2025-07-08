# Files Storage - crypto

### Solution

Serwer przy uploadzie liczy (hash) nazwę folderu, do której potem wsadza pliki. Ktoś wcześniej napisał [hashXorBreaker.py](github.com/malt3/sha256-xor-collisions/blob/master/hashXorBreaker.py), który użyłem do wygenerowania plików których hashe po zXORowaniu dadzą target hash (folder z flagą: `b0e9b3e3ae021b54eefca53e3a06a47d758198d7163edc054f8ee1456e491f20`)

```python
import os
import secrets
from hashxorbreaker import HashBreaker

if __name__ == "__main__":
    hb = HashBreaker()
    hb.generateLUT()

    os.mkdir("./outputs")

    wanted_hash = bytes.fromhex(
        "b0e9b3e3ae021b54eefca53e3a06a47d758198d7163edc054f8ee1456e491f20"
    )
    previous_hash = bytes.fromhex(
        "936a185caaa266bb9cbe981e9e05cb78cd732b0b3280eb944412bb6f8f8f07af"
    )
    inputs = hb.alterHash(previous_hash, wanted_hash)

    with open("./outputs/base.txt", "ab") as f:
        f.write(b"helloworld")

    for entry in inputs:
        with open("./outputs/" + secrets.token_hex(6) + ".txt", "ab") as f:
            f.write(entry)

```

Flaga: `ecsc25{HashMeBabyOneMoreTime_72615207c}`