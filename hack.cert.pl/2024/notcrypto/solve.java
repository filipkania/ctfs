import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.spec.KeySpec;
import java.util.Base64;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import java.util.Objects;

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

class C {
    private final Integer index;

    public C(Integer index) {
        this.index = index;
    }

    public C(Character c) {
        this.index = (int) c;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        C a = (C) o;
        return index == a.index;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(index);
    }
}
