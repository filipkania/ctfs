# QuiRks - stegano

### Solution

Kod QR ma zakodowaną flagę w różnych typach sekcji (mają one długość 0). Można pobrać bibliotekę [gozxing](https://github.com/makiuchi-d/gozxing), którą można łatwo zpatchować:

```patch
diff --git a/qrcode/decoder/decoded_bit_stream_parser.go b/qrcode/decoder/decoded_bit_stream_parser.go
index be4568e..3fcd6ad 100644
--- a/qrcode/decoder/decoded_bit_stream_parser.go
+++ b/qrcode/decoder/decoded_bit_stream_parser.go
@@ -1,6 +1,8 @@
 package decoder
 
 import (
+       "fmt"
+
        "golang.org/x/text/encoding"
        "golang.org/x/text/transform"
 
@@ -30,6 +32,8 @@ func DecodedBitStreamParser_Decode(
        var mode *Mode
        var e error
 
+       out := ""
+
        for {
                // While still another segment to read...
                if bits.Available() < 4 {
@@ -108,11 +112,19 @@ func DecodedBitStreamParser_Decode(
                                if e != nil {
                                        return nil, e
                                }
+
+                               if count == 0 {
+                                       out += "0"
+                               }
                        case Mode_BYTE:
                                result, byteSegments, e = DecodedBitStreamParser_decodeByteSegment(bits, result, count, currentCharacterSetECI, byteSegments, hints)
                                if e != nil {
                                        return nil, e
                                }
+
+                               if count == 0 {
+                                       out += "1"
+                               }
                        case Mode_KANJI:
                                result, e = DecodedBitStreamParser_decodeKanjiSegment(bits, result, count)
                                if e != nil {
@@ -129,6 +141,8 @@ func DecodedBitStreamParser_Decode(
                }
        }
 
+       fmt.Println(out)
+
        if currentCharacterSetECI != nil {
                if hasFNC1first {
                        symbologyModifier = 4
```

```bash
⋊> ~/s/h/q/reader go run .
1100101011000110111001101100011001100100011010001111011001101010111010000110011011001110011010001101110001100000101111101100111001100000110010001111101
Not a flag 416C736F206E6F74206120666C6167 101010001110010011110010010000001101000011000010111001001100100011001010111001000100001 https://youtu.be/t-bgRQfeW64
```

Output trzeba zpadować jedną jedynką z lewej strony i otrzymujemy flagę:
`ecsc24{5t3g4n0_g0d}`