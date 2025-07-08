# Photo Archiver - web

### Vulnerability

DNS rebinding attack

### Solution

Zadanie polega na wyeksploitowaniu tego, że pomiędzy sprawdzeniem adresu domeny mija trochę czasu zanim skrypt dopiero zacznie pobierać plik.
W tym czasie można zmienić adres na taki odpowiadający localhostowi.

Drugi bug jest w sprawdzaniu extensiona zdjęcia, serwer sprawdza czy link kończy się z `(.png|.jp(e?)g)`, jeśli tak, przepuszcza request.
Można to zbypassować używając hashtaga: `flag#.jpg`

Do ataku użyłem [tego toola](http://dnsrebindtool.43z.one/), ustawia TTL na 5 sekund, więc najpierw zqueryowałem lokalnie i po ~4 sekundach wysłałem na remote'a link:
`http://xxxxxxx.1-1-1-1.127-0-0-1.rebind.43z.one:23612/flag#.jpg`

`ecsc25{TOCTOU-is-a-weird-acronym}`
