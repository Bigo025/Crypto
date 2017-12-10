from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


key = DSA.generate(2048)
signer = DSS.new(key, 'fips-186-3')
sha = SHA256.new("AZE".encode())
signature = signer.sign(sha)
print(signature)
verifier = DSS.new(key.publickey(), 'fips-186-3')
try:
  verifier.verify(sha, signature)
  print("The signature is authentic.")
except ValueError:
  print("Error :The signature is not authentic.")