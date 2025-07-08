# Enter the Matrix - crypto

### Solution

~~Zapytać Gemini 2.5 Pro~~ Rozwiązać samemu używając LLL

```python
n = ...
coeffs = [...]
result = ...

from sage.all import vector, power_mod, Matrix, ZZ

size = len(coeffs)
a = vector(coeffs + [-result])
dim = size + 1
try:
    inv_a = power_mod(a[-1], -1, n)
except ValueError:
    print("Error: -result is not invertible modulo n.")
    exit()

B = Matrix(ZZ, dim, dim)

for i in range(size):
    B[i, i] = 1
    B[i, dim - 1] = (-a[i] * inv_a) % n

B[dim - 1, dim - 1] = n

reduced_B = B.LLL()
solution_vector = reduced_B[0]

if solution_vector[-1] == -1:
    solution_vector = -solution_vector

flag_bytes = solution_vector[:size]
flag = "".join(chr(byte) for byte in flag_bytes)

print("Found flag:")
print(flag) # ecsc25{apparently_LLL_is_now_baby_crypto}
```