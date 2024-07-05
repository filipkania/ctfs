# The zettabyte file search - forensics

### Task

Obraz dysku ZFS z brakami w uberblokach/zreformatowanym ZFS'em.

### Solution

Analizując obraz, widać że istnieje plik `flag.webp`, który musimy odzyskać.

Można użyć `photorec`'a, żeby wyeksportować wszystkie `.webp` (zaznaczyć `RIFF` format).

![](./f19048408.webp)
