![](../images/Pasted%20image%2020220717200134.png)

Po przeczytaniu hinta, widać że w kodzie została wyłączona funkcja sprawdzania nowych linii oraz walidacji headerów. Dodatkowo po przeanalizowaniu pliku `default.conf` flagę można dostać tylko jeśli header `X-Real-IP` jest ustawiony na `127.0.0.1`

Wybrany klient HTTP/3: https://github.com/aiortc/aioquic (zawiera example client)

Payload z header injection:
![](../images/Pasted%20image%2020220717202306.png)

Po użyciu `python client.py https://quiclookthis.ecsc22.hack.cert.pl:18443/ --insecure` otrzymujemy flagę:
![](../images/Pasted%20image%2020220717202432.png)