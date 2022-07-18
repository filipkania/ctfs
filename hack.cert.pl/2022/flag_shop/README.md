![](../images/Pasted%20image%2020220717211501.png)

Decode APK'a z `apkutil` pokazał, że jest to appka napisana w React-Native, `file` na `index.android.bundle` wskazał, że jest to Hermes Bytecode v.84.

Fork `hbctool` dla wersji 84 bytecode'u: https://github.com/niosega/hbctool/tree/draft/hbc-v84

Dekompilacja bytecode'u przy użyciu: `hbctool disasm index.android.bundle aaa`

Usunięcie instrukcji `JLess, LoadConstFalse i Ret` w funkcji `checkBalance`:

![](../images/Pasted%20image%2020220717212333.png)

Ponowne pakowanie appki:
```
hbctool asm aaa index.android.bundle
apkutil b FlagShop-preprod-5e46b4604bf49360100dd2ef2af34c33fe4379cb
adb install ./FlagShop-preprod-5e46b4604bf49360100dd2ef2af34c33fe4379cb.patched.apk
```

Po usunięciu instrukcji, możemy kupić flagę nawet gdy nie mamy wymaganej ilości pieniędzy do tego:![](../images/Pasted%20image%2020220717212654.png)