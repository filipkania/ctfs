# Over The Domain - stegano

### Task

W załączniku znajduje się pcap, który ma w sobie requesty DNS.

### Solution

Przejść przez wszystkie requesty DNS'owe i zdebase64'ować je:

```
⋊> ~/s/h/over-the-domain python analyze.py | grep -i '^[A-Za-z0-9_\'{}]*$'
b'{th1s_w4s_n0'
b't_mean7_t0_b'
⋊> ~/s/h/over-the-domain python analyze.py | grep -i '[3e]_'
b'c^\'4e_"(S#*N'
b'3_s33n}\nPK\x01\x02'
b">rx[J'eE_`96"

# ecsc24{th1s_w4s_n0t_mean7_t0_b3_s33n}
```
