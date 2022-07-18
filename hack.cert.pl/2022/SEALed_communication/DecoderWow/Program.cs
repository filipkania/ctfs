using Encryption;
using Microsoft.CSharp.RuntimeBinder;
using Microsoft.Research.SEAL;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Device.Location;
using System.IO;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;

namespace Client
{
    internal class Program
    {
        private static async Task Main(string[] args)
        {
            string path = "c:\\secretagent\\publickey.key";
            SecretKey secretKeyToSecretKey = BFVEncryptionUtils.ParseBase64EncodedSecretKeyToSecretKey(File.ReadAllText("c:\\secretagent\\secretkey.key"));
            PublicKey publicKeyToPublicKey = BFVEncryptionUtils.ParseBase64EncodedPublicKeyToPublicKey(File.ReadAllText(path));
            BFVEncryptionProvider encryptionProvider = new BFVEncryptionProvider();
            Decryptor decryptor = new Decryptor(encryptionProvider.GetSEALContext(), secretKeyToSecretKey);
            IntegerEncoder encoder = new IntegerEncoder(encryptionProvider.GetSEALContext());
            Encryptor encryptor = new Encryptor(encryptionProvider.GetSEALContext(), publicKeyToPublicKey, secretKeyToSecretKey);

            JObject data = JObject.Parse(File.ReadAllText(@"c:\secretagent\data.txt"));
            Console.WriteLine(data.GetValue("guid"));

            Ciphertext longitude = BFVEncryptionUtils.ParseBase64EncodedCiphertextToCiphertext(data.GetValue("longitude").ToString());
            Plaintext decodedL = new Plaintext();
            decryptor.Decrypt(longitude, decodedL);
            Console.WriteLine(Convert.ToDouble(encoder.DecodeInt32(decodedL).ToString()) / 1000000.0);

            Ciphertext latitude = BFVEncryptionUtils.ParseBase64EncodedCiphertextToCiphertext(data.GetValue("latitude").ToString());
            Plaintext decodedLa = new Plaintext();
            decryptor.Decrypt(latitude, decodedLa);
            Console.WriteLine(Convert.ToDouble(encoder.DecodeInt32(decodedLa).ToString()) / 1000000.0);

        }
    }
}
