# Magiczna cat - re

### Task

Gra napisana w [Haxe](https://haxe.org/use-cases/games/), która wymaga hasła, żeby dostać flagę.

### Solution

Po zobaczeniu, że żeby dostać flagę trzeba wpisać tajemnicze hasło, możemy zbruteforce'ować je:
```javascript=
let chars = "";
while(true) {
    for (let x = 0; x < 0xff; x++) {
        var ok = false;
        var _g = 0;
        var _g1 = Main_checks;
        while(_g < _g1.length) {
            var c = _g1[_g];
            ++_g;
            var code = x;
            var h = haxe_crypto_Sha256.encode(Main_entry + String.fromCodePoint(code));
            if(h == c) {
                var code1 = x;
                Main_entry += String.fromCodePoint(code1);
                console.log(Main_entry)
                chars += String.fromCodePoint(x);
                ok = true;
                break
            }
        }
    }

    if(Main_checks.length == Main_entry.length) {
        console.log(chars);
        var key = haxe_io_Bytes.ofString(Main_entry);
        var msg = haxe_io_Bytes.ofHex(Main_puma);
        var totallyNotRc4 = new haxe_crypto_RC4();
        totallyNotRc4.init(key);
        var data = totallyNotRc4.encrypt(msg).toString();
        console.log(data);
        break
    }
}
```

Po zdecryptowaniu `Main_puma` hasłem `SPEAKCHONKERANDENTER`, dostajemy flagę:
`ecsc24{A_cat_from_my_past_btw_the_language_is_called_haxe}`