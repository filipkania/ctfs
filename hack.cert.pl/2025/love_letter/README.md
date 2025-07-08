# Love letter - re

### Solution

W zadaniu dostajemy binarkę z "malwarem", która jest w dziwny sposób spakowana/zencryptowana

- Odpaliłem ją w WinDbg triggerując anti-debugging prompt (żeby proces się nie zamknął) i zdumpowałem odszyfrowaną Scyllą
- Po wczytaniu jej do dekompilera, widać że w `_TLS_Entry_0()` jest logika do wykrywania czy process jest debuggowany, odpala też funkcję `sub_11220()` jeśli nie jest
- Wypatchowałem wszystkie jumpy żeby zawsze funkcja `sub_11220()` się wykonywała (nawet jeśli proces jest debuggowany):
  ![](../images/e1634023-d56c-4623-8acb-db01b19578ed.png)
- Potem odpaliłem ją w debuggerze Binjy, breakpointując na funkcji dekrypcji (chyba RC4):
  ![](../images/5273acd6-8fc5-47c0-a907-4998ba8a30ad.png)
- Po breakpointcie (i stepie przez `*1=1`) ustawiłem RIP na adres RBX'u, który wskazywał na adres shellcode'u
- Kolejny breakpoint na instrukcje po loopie XORującym shellcode, po nim flaga była w zdecryptowanym shellcode'zie:
  ![](../images/7855fe13-10bf-4403-980d-e6eea76640c8.png)
