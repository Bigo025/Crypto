import sys
import socket
import select
from threading import Thread
from Crypto.PublicKey import RSA
import hashlib

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadWalletListen(Thread):

  def __init__(self, relaySocket):
    Thread.__init__(self)
    self.connectionToRelay = relaySocket

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while True :
      msg = receiveAndDecode(self.connectionToRelay)
      print("Reçu Relay: {}".format(msg))

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadWalletWrite(Thread):

  def __init__(self, relaySocket):
    Thread.__init__(self)
    self.connectionToRelay = relaySocket

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while True :
      msg = input()
      encodeAndSend(self.connectionToRelay, msg)

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def wallet(hostName, hostPort):
  #Connexion en client sur le master
  connectionToRelay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connectionToRelay.connect((hostName, hostPort))
  print("Connection established with Relay on port {}".format(hostPort))

  encodeAndSend(connectionToRelay, "0") #s'identifie au relay en tant que wallet

  thread1 = ThreadWalletListen(connectionToRelay)
  thread2 = ThreadWalletWrite(connectionToRelay)

  thread1.start()
  thread2.start()

def encodeAndSend(toSocket, message):
  msg = message.encode()
  toSocket.send(msg)

def receiveAndDecode(fromSocket):
  msg = fromSocket.recv(1024)
  message = msg.decode()
  return message

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------



def fetch_key(name, password):	
  """
  The following code reads the private RSA key back in, and then create public addresse.
  return : publickey and  public addresse
  """
  file = open(name+".bin", "rb").read()
  key = RSA.import_key(file, passphrase=password)
  
  sha = hashlib.sha256()
  sha.update(key.publickey().exportKey())
  
  ripemd = hashlib.new('ripemd160')
  ripemd.update(sha.digest())
  
  #RIPEMD160 to derive addresses from public keys
  address = ripemd.hexdigest()
  print(" Addresse : ", address)
  
  #print(key.publickey().exportKey())
  return (key.publickey().exportKey(), address) 
	
#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def main():
  publicKey = None 
  publicAddress = None
  if len(sys.argv) != 5:
    print("Il faut mettre une adresse Ip, un port, Nom du wallet et mot de passe")
    sys.exit(1)

  else:
    wallet(sys.argv[1],int(sys.argv[2]))
    # call fetch_key 
    publicKey, publicAddress = fetch_key(sys.argv[3],sys.argv[4])


if __name__ == '__main__':
  main()