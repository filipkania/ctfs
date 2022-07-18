![](../images/Pasted%20image%2020220717212758.png)

Kodowanie jednego znaku powstaje przez `XOR` danego znaku, następnego znaku oraz `$keyi` poprzedniego znaku. Znamy 5 pierwszych znaków flagi, więc wszystko co potrzebujemy do zdekodowania flagi to crc32. Potem wystarczy zbruteforce'ować 

Po paru minutach bruteforce'owania otrzymujemy flagę:

![](../images/Pasted%20image%2020220718113601.png)