# Sneaky Train - re

### Solution

Dostajemy binarkę ze snake'iem, po ~4 zjedzonych punktów gra freezuje się i czeka na wpisanie hasła

Po dekompilacji widać że binarka kopiuje hasło do variabla i zmienia pierwsze litery hasła na "secret":

![](../images/1f12ba28-cbbf-4f2c-934e-0f626cb88b2a.png)

![](../images/c7402916-4b32-4431-909e-a814214c69f7.png)

Po haśle (`secretxxx`) możemy dokończyć grę (tak długo aż długość węża nie będzie równała się długości flagi).

Flaga: `ecsc25{all_rights_reversed!!1}`