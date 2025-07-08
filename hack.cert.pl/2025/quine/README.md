# Quine - re

### Solution

W zadaniu dostajemy binarkę z logiką VM'ki + bytecode

Po x promptach z zdekompilowanym kodem, LLM wypluł reimplementacje VMki w Pythonie, później po "zinlineowaniu" bytecodeu (hash funkcję są constantami: f1 = 2, f2 = 6), użyłem Z3 żeby znaleźć symbolicznie flagę:

```python
import z3
import hashlib

f1_2 = 2
f2_3 = 6
c = f1_2 ^ f2_3
c_bv = z3.BitVecVal(c, 3)

output = [2, 5, 4, 2, 3, 7, 0, 3, 5, 3, 3, 7, 2, 5, 3, 7, 7, 6, 6, 0]

solver = z3.Solver()
AX = z3.BitVec('AX', 64)

for k in range(20):
    ax_k = z3.LShR(AX, 3 * k)
    cx1 = z3.Extract(2, 0, ax_k)
    bx = z3.BitVecVal(f1_2, 3) ^ cx1
    ax_k1 = z3.LShR(AX, 3 * k + 3)
    cx2 = z3.BitVecVal(f2_3, 3)
    bx = bx ^ cx2
    cx3 = z3.Extract(2, 0, ax_k1)
    bx = bx ^ cx3
    ok_bv = z3.BitVecVal(output[k], 3)
    solver.add(ok_bv == bx)

if solver.check() == z3.sat:
    model = solver.model()
    ax_val = model[AX].as_long()
    key = ax_val ^ 0x48C8CE7C0A532EC7
    key_bytes = key.to_bytes(8, 'big')

    try:
        key_str = key_bytes.decode('ascii')
        print(f"Flag: ecsc25{{{key_str}}}") # ecsc25{AoC24d17}
    except UnicodeDecodeError:
        print(f"Key found but not ASCII: {key_bytes.hex()}")
else:
    print("No solution found")
```