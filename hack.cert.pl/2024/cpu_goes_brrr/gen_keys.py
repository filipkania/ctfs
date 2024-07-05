from multiprocessing import Pool
from sympy import isprime
import binascii
import sys

sys.setrecursionlimit(55000)

flag_enc = binascii.unhexlify(
    "6e687808b07745006f898b04bce8c2993bdc0b434f217256c8dde3e846ed94d76f0501f4bf"
)

cache = {}
def tribonacci(n):
  if n in cache:
    return cache[n]

  if n < 2:
      return 1
  else:
    res = ((tribonacci(n - 1) & 0xFFFFFFFFFFFFFFFF) + (tribonacci(n - 2) & 0xFFFFFFFFFFFFFFFF) + (tribonacci(n - 3) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    cache[n] = res
    return res

def sub_1230(arg1: int) -> int:
    rax_2 = 0
    var_1c = arg1
    while True:
        rax_2 = tribonacci(var_1c)
        if isprime(rax_2):
            break

        var_1c += 1

    return rax_2

def sub_126b(i: int) -> int:
    var_1a = sub_1230(i)
    return ~var_1a & 0xffffffff


if __name__ == "__main__":
    args = [i ** 3 for i in range(len(flag_enc))]
    with Pool(5) as p:
        res = p.map(sub_126b, args)

    print(f"{res=}")
