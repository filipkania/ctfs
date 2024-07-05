# notCrypto - misc

### Vulnerability

W zmiennej `secrets` range jest off-by-one i ma w sobie wartości od <0x0; 0xfffe>.

### Solution

Korzystając z tego vulna, można wysłać payload `\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff`, który spowoduje że hasło to będzie: `"null" * 11`.

```java
class Main {
    public static void main(String[] args) throws Exception {
        // python -c 'print("\uffff" * 11); input()' | nc notcrypto.ecsc24.hack.cert.pl 5103
        String enc_flag = "INNb6+40E6zZ2Sp6pnpwy/5uB6Lte0dWH4721kv2xLl/EiE+AsYAdx16GHln2CV9Vxya+g7QFQWmkEq3sHvTOA==";

        String flag = (new Decryptor()).decrypt(enc_flag);
        System.out.println(flag);
    }
}

class Decryptor {
    private final Map<C, String> secrets = IntStream.range(Character.MIN_VALUE, Character.MAX_VALUE)
            .mapToObj(C::new)
            .collect(Collectors.toMap(
                    Function.identity(),
                    c -> UUID.randomUUID().toString()
            ));

    String generateRandomPassword(String userInput) {
        return userInput.chars()
                .mapToObj(i -> (char) i)
                .map(C::new)
                .map(secrets::get)
                .collect(Collectors.joining());
    }

    SecretKey getKeyFromPassword(String password) throws Exception {
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), "Why so salty?".getBytes(), 65536, 256);
        return new SecretKeySpec(factory.generateSecret(spec).getEncoded(), "AES");
    }

    public String decrypt(String flag) throws Exception {
        SecretKey key = getKeyFromPassword(generateRandomPassword("\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff\uffff"));
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] cipherText = cipher.doFinal(Base64.getDecoder().decode(flag));
        return new String(cipherText);
    }
}
```

`ecsc24{integer_cache_and_2_byte_chars_#justjavathings}`