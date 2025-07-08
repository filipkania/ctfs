# Levelled MFA - web - crypto

### Solution

Zadanie podobne do poprzedniego (Easy MFA), tym razem zamiast wbudowanego Pythonowego randoma, serwer korzysta z LCG z predefiniowanym modulusem, multiplierem (i counterem=0).

Korzystając z [truncated_state_recovery.py](https://github.com/jvdsn/crypto-attacks/blob/master/attacks/lcg/truncated_state_recovery.py) i 64-ech 8-bajtowych stringów można przewidzieć state LCG i cofnąć się do generowania JWT sekretu. 

[solve script](./exp.py)

`ecsc25{1_h0pe_it_w4s_n0t_just_ch4tgp7_vib1ng}`
