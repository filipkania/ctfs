# Maze Runner - misc

### Solution

Sandbox musi zwrócić tylko 1 i 0, więc można wyexfilować flagę binarnie, blokami po 96 bitów (12 bajtów/znaków):

```python
import os
n = 4
print([int(x) for x in "".join([format(ord(x), 'b').zfill(8) for x in os.popen("cat flag.txt").read()])][96 * n: 96 * (n + 1)])
print("\n" * 1000) # filling the buffer

return 1
```

Flaga: `ecsc25{the_r3al_m4ze_was_th3_fr1ends_we_m4de_al0ng_the_way!}`
