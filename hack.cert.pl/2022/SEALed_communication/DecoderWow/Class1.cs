using Microsoft.Research.SEAL;
using System;
using System.IO;
using System.Text;

namespace Encryption
{
    public static class BFVEncryptionUtils
    {
        public static string ParseCipherTextToBase64(Ciphertext ciphertext)
        {
            MemoryStream memoryStream = new MemoryStream();
            ciphertext.Save((Stream)memoryStream);
            memoryStream.Seek(0L, SeekOrigin.Begin);
            return new StreamReader(BFVEncryptionUtils.ConvertToBase64((Stream)memoryStream)).ReadToEnd();
        }

        public static Ciphertext ParseBase64EncodedCiphertextToCiphertext(
          string base64EncodedCiphertext)
        {
            EncryptionParameters parms = new EncryptionParameters(SchemeType.BFV);
            ulong polyModulusDegree = 4096;
            parms.PolyModulusDegree = polyModulusDegree;
            parms.CoeffModulus = CoeffModulus.BFVDefault(polyModulusDegree);
            parms.PlainModulus = new Modulus(512UL);
            SEALContext context = new SEALContext(parms);
            MemoryStream memoryStream = new MemoryStream(Convert.FromBase64String(base64EncodedCiphertext));
            Ciphertext ciphertextToCiphertext = new Ciphertext(context);
            ciphertextToCiphertext.Load(context, (Stream)memoryStream);
            return ciphertextToCiphertext;
        }

        public static string ParseSecretKeyToBase64(SecretKey secretKey)
        {
            MemoryStream memoryStream = new MemoryStream();
            secretKey.Save((Stream)memoryStream);
            memoryStream.Seek(0L, SeekOrigin.Begin);
            return new StreamReader(BFVEncryptionUtils.ConvertToBase64((Stream)memoryStream)).ReadToEnd();
        }

        public static string ParsePublicKeyToBase64(PublicKey publicKey)
        {
            MemoryStream memoryStream = new MemoryStream();
            publicKey.Save((Stream)memoryStream);
            memoryStream.Seek(0L, SeekOrigin.Begin);
            return new StreamReader(BFVEncryptionUtils.ConvertToBase64((Stream)memoryStream)).ReadToEnd();
        }

        public static SecretKey ParseBase64EncodedSecretKeyToSecretKey(
          string base64EncodedSecretKey)
        {
            EncryptionParameters parms = new EncryptionParameters(SchemeType.BFV);
            ulong polyModulusDegree = 4096;
            parms.PolyModulusDegree = polyModulusDegree;
            parms.CoeffModulus = CoeffModulus.BFVDefault(polyModulusDegree);
            parms.PlainModulus = new Modulus(512UL);
            SEALContext context = new SEALContext(parms);
            MemoryStream memoryStream = new MemoryStream(Convert.FromBase64String(base64EncodedSecretKey));
            SecretKey secretKeyToSecretKey = new SecretKey();
            secretKeyToSecretKey.Load(context, (Stream)memoryStream);
            return secretKeyToSecretKey;
        }

        public static PublicKey ParseBase64EncodedPublicKeyToPublicKey(
          string base64EncodedPublicKey)
        {
            EncryptionParameters parms = new EncryptionParameters(SchemeType.BFV);
            ulong polyModulusDegree = 4096;
            parms.PolyModulusDegree = polyModulusDegree;
            parms.CoeffModulus = CoeffModulus.BFVDefault(polyModulusDegree);
            parms.PlainModulus = new Modulus(512UL);
            SEALContext context = new SEALContext(parms);
            MemoryStream memoryStream = new MemoryStream(Convert.FromBase64String(base64EncodedPublicKey));
            PublicKey publicKeyToPublicKey = new PublicKey();
            publicKeyToPublicKey.Load(context, (Stream)memoryStream);
            return publicKeyToPublicKey;
        }

        private static Stream ConvertToBase64(Stream stream)
        {
            byte[] array;
            using (MemoryStream destination = new MemoryStream())
            {
                stream.CopyTo((Stream)destination);
                array = destination.ToArray();
            }
            return (Stream)new MemoryStream(Encoding.UTF8.GetBytes(Convert.ToBase64String(array)));
        }
    }
}

namespace Encryption
{
    internal class BFVEncryptionProvider
    {
        private SEALContext Context { get; set; }

        private KeyGenerator Keygen { get; set; }

        public BFVEncryptionProvider()
        {
            EncryptionParameters parms = new EncryptionParameters(SchemeType.BFV);
            ulong polyModulusDegree = 4096;
            parms.PolyModulusDegree = polyModulusDegree;
            parms.CoeffModulus = CoeffModulus.BFVDefault(polyModulusDegree);
            parms.PlainModulus = new Modulus(512UL);
            this.Context = new SEALContext(parms);
            this.Keygen = new KeyGenerator(this.Context);
        }

        public PublicKey GetPublicKey() => this.Keygen.PublicKey;

        public SecretKey GetSecretKey() => this.Keygen.SecretKey;

        public Encryptor GetEncryptor() => new Encryptor(this.Context, this.GetPublicKey());

        public Decryptor GetDecryptor() => new Decryptor(this.Context, this.GetSecretKey());

        public Evaluator GetEvaluator() => new Evaluator(this.Context);

        public IntegerEncoder GetIntegerEncoder() => new IntegerEncoder(this.Context);

        public SEALContext GetSEALContext() => this.Context;
    }
}