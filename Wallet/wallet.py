import sys
import socket
import select
from threading import Thread
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import hashlib
import pickle
from datetime import datetime
from os import path
sys.path.append(path.abspath('../Utils'))
from Blocks import Block
from util import *

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
      lastBlock = receiveAndDecode(self.connectionToRelay)


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
      global privateKey 
      global publicKey
      global publicAddress
      privateKey, publicKey, publicAddress = fetch_key(sys.argv[3],sys.argv[4])
      print("********************************************************** \n")
      print(" Adresse publique ", publicAddress)
      print("********************************************************** \n")
      print(" Pour une nouvelle transaction entez : ")
      recipient = input(" L'addresse du recipient  : ")
      amount = input(" Montant  : ")
      time = str(datetime.now())
      data = str(publicAddress) + recipient + amount + time
      signature = sign_transaction(privateKey, data.encode())
      dataToSend = send_format(publicKey, signature, str(publicAddress), recipient, amount, time)
      
      encodeAndSend(self.connectionToRelay, dataToSend)
      print(" Montant envoyé")
      print("********************************************************** \n")

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
  msg = pickle.dumps(message)
  toSocket.send(msg)

def receiveAndDecode(fromSocket):
  msg = fromSocket.recv(10000)
  message = pickle.loads(msg)
  return message

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------



def fetch_key(name, password):	
  """
  The following code reads the private DSA key back in, and then create public addresse.
  return : publickey and  public addresse
  """
  file = open(name+".pem", "rb").read()
  key = DSA.import_key(file, passphrase=password)
  
  sha = hashlib.sha256()
  sha.update(key.publickey().exportKey())
  
  ripemd = hashlib.new('ripemd160')
  ripemd.update(sha.digest())
  
  #RIPEMD160 to derive addresses from public keys
  address = ripemd.hexdigest()
  #print("-----------------------------------------------------------------------------")
  #print(key.publickey().exportKey())
  return (key, key.publickey(), address) 
	
#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def sign_transaction(privateKey, data):
  """
  return the publicKey, the signature and the hashed transaction (so we can send this to the relay node).
  """
  sha = SHA256.new(data)
  signer = DSS.new(privateKey, 'fips-186-3')
  signature = signer.sign(sha)
  return(signature)
  

    

def send_format(publicKey, signature, senderAddress, receiverAddress, amount, time):
  data = [publicKey.exportKey(), signature, senderAddress, receiverAddress, amount, time]
  return data
	
#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def main():

  if len(sys.argv) != 5:
    print("Il faut mettre une adresse Ip, un port, Nom du wallet et mot de passe")
    sys.exit(1)

  else:
    wallet(sys.argv[1],int(sys.argv[2]))
    # call fetch_key 
    


if __name__ == '__main__':
  privateKey = None
  publicKey = None 
  publicAddress = None
  main()