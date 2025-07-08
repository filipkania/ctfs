# Easy MFA - web - crypto

### Solution

W zadaniu dostajemy 384 64-bitowe random stringi, korzystając z tego że Python korzysta z Mersienne Twistera (którego da się odwrócić), jesteśmy w stanie przewidzieć wcześniejsze i następne wartości.

Żeby odwzorować cały state, potrzebujemy 624 32-bitowe wartości, my dostajemy 64-bitowe outputy, więc trzeba dodatkowo zrobić 2 operacje (`x >> 32`) i (`x & 0xFFFFFFFF`) żeby wsadzić je do Untwistera

Potem trzeba wygenerować JWT secret który używamy do zforgeowania poprawnego tokena z `username=admin`

[solve script](./exp.py)

Flaga: `ecsc25{that_w4s_s0_rand0m}`
