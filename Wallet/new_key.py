from Crypto.PublicKey import DSA
import sys


def generate_key(name, password):
	"""
	generates a new DSA key pair (secret) and saves it into a file, protected by a password.
	"""


	key = DSA.generate(2048)
	# AES128 to encrypt private keys
	encryptKey = key.exportKey(passphrase=password, protection="scryptAndAES128-CBC")

	file = open(name+".pem", "wb")
	file.write(encryptKey)
	#print(key.publickey().exportKey())
	file.close()
  


	
def main():
  
  if len(sys.argv) != 3:
    print("Il faut mettre un nouveau Nom et un mot de passe ")
    sys.exit(1)

  else:
    generate_key(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
  main()
