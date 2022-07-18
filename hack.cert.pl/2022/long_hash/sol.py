import binascii

res = [str(hex(x))[2:] for x in [7233978899669148517, 8020473808943215955, 6368781824082329972, 7233978869803283055, 9042790924356318547]]
flag = b""

for x in res:
  flag += binascii.unhexlify(x)[::-1]

print(flag)