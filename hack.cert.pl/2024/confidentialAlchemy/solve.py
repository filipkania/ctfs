import itertools
import string
import hashlib
import binascii

from tqdm import tqdm

data = binascii.unhexlify("f11323f60f914e33c291c7d8c69b24025f544b352b2132702d5613481721122b574105475a04750f564047080a055150075e525a507a4275026a2d5a036644420f52053517025256094560575266525e7d7d59774f70634d2d567d056d50620955690416486b424e772b785e32643063343637393035313966633036393666336236343363663365633930363136")

known_text = "U2FsdGVkX1"
recovered_secret = []

printables = set(string.printable)
printables.add("\x00")

for i, d in enumerate(data[:len(known_text)]):
  for x in range(0xff + 1):
    if chr(d ^ x) == known_text[i]:
      recovered_secret.append(x)
      break
  else:
    print("not found")
    exit(1)

print(binascii.hexlify(bytes(recovered_secret)))

def xor(*t):
  from functools import reduce
  from operator import xor
  return "".join([chr(reduce(xor, x, 0)) for x in zip(*t)])

base64_alphabet = string.ascii_letters + string.digits + "+/"
for guess in tqdm(itertools.product(base64_alphabet, repeat=(14 - len(known_text))), total=len(base64_alphabet) ** (14 - len(known_text))):
  guess_secret = recovered_secret[:]
  for i, v in enumerate(guess):
    guess_secret.append(data[len(known_text) + i] ^ ord(v))

  h = hashlib.new("sha512")
  h.update(bytes(guess_secret))
  for x in [ord(x) for x in h.hexdigest()]:
    guess_secret.append(x)

  xored = xor(data, guess_secret)

  if set(xored).issubset(printables):
    print(f"---\nfound something: {bytes(xored.encode())=}, {binascii.hexlify(bytes(guess_secret))=}")
