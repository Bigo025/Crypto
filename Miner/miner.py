import sys
import socket
import select
import hashlib
import struct
import codecs
import time
import random
from threading import Thread
import pickle

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadMinerListenRelay(Thread, transactions):

  def __init__(self, relaySocket):
    Thread.__init__(self)
    self.connectionToRelay = relaySocket
    self.transactionsToMine = transactions

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    
    global previousBlock
    
    while(True):

      msg = receiveAndDecode(self.connectionToRelay)
      print("Transaction : {}".format(msg))

      if (msg == "Stop") : #Message pour stop car un block a été trouvé par quelqu'un
        stopMinerWork()
      
      elif (msg[0] == "x") :
        previousBlock = msg[1:]
      
      elif (msg[0] == "t") : #C'est une transaction 
        self.transactionsToMine.append(msg)


      msg = "["+msg+"]"
      print("Bloc -> {}".format(msg))
      encodeAndSend(self.connectionToRelay, msg)

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadMinerWork(Thread):

  def __init__(self, transactions, blockMined, previousBlock):
    Thread.__init__(self)
    self.transactionsToMine = transactions
    self.block = blockMined
    self.previousBlock = previousBlock
    self.stop = False

  def run(self):
    found = False
    transactionsList = self.transactionsToMine[:]
    nonce = random.randint(0, 1000000000)
    compteur = 0
    prev_block = self.previousBlock
    while (not found or not self.stop):
      mrklroot = self.calculateMerkleRoot(transactionsList)
      date = int(time.time()) # 2014-02-20 04:57:25
      bits = 0x1fffffff
      # https://en.bitcoin.it/wiki/Difficulty
      # Difficulté établie à 4 zéros
      exp = bits >> 24
      mant = bits & 0x3fff
      target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
      target_str = codecs.decode(target_hexstr, 'hex')

      header = ( codecs.decode(prev_block[::-1], 'hex') +
                codecs.decode(mrklroot[::-1], 'hex') + struct.pack("<LLL", date, bits, nonce))
      hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
      print(nonce, codecs.encode(hash[::-1], 'hex'))
      if ((hash[::-1] < target_str) and self.previousBlockStillTheSame(prev_block) and self.merkleRootStillTheSame(mrklroot)):
        print('success')
        print(compteur)
        found = True
      nonce += 1
      if nonce==1000000000:
        nonce=1
      compteur +=1


  def merkleRootStillTheSame(self, currentMerkleRoot):
    transactionsList = self.transactionsToMine[:]
    newMerkleRoot = self.calculateMerkleRoot(transactionsList)
    return newMerkleRoot == currentMerkleRoot

  def calculateMerkleRoot(self, transactionsList):
    tmpTransactionsList = transactionsList
    newTransactionsList = []
    
    for i in range(0, len(tmpTransactionsList), 2):
      leftTransaction = tmpTransactionsList[i]
      if (i+1 != len(tmpTransactionsList)):
        rightTransaction = tmpTransactionsList[i+1]
      else:
        rightTransaction = ""
        
      # hash
      hashLeftTransaction = hashlib.sha256(leftTransaction.encode())
      if rightTransaction != "":
        hashRightTransaction = hashlib.sha256(rightTransaction.encode())
      
      if rightTransaction != "":
        newTransactionsList.append(hashLeftTransaction.hexdigest() + hashRightTransaction.hexdigest())
      else:
        newTransactionsList.append(hashLeftTransaction.hexdigest())
    if len(tmpTransactionsList) != 1:
      transactionsList = newTransactionsList
      calculateMerkleRoot(transactionsList)
    return transactionsList[0]

  def previousBlockStillTheSame(self, currentPreviousBlock):
      return currentPreviousBlock == self.previousBlock
  
  def stopThread(self):
    self.stop = True

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def miner (hostName, hostPort):
  
  connectionToRelay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connectionToRelay.connect((hostName, hostPort))
  print("Connection established with Relay on port {}".format(hostPort))

  encodeAndSend(connectionToRelay, "1") #s'identifie au relay en tant que miner

  global thread1
  global thread2
  global block
  global transactions
  
  block = None
  transactions = receiveAndDecode(connectionToRelay)


  thread1 = ThreadMinerListenRelay(connectionToRelay, transactions)
  thread2 = ThreadMinerWork(transactions, block)
  
  thread1.start()
  thread2.start()

def encodeAndSend(toSocket, message):
  msg = pickle.dumps(message)
  toSocket.send(msg)

def receiveAndDecode(fromSocket):
  msg = fromSocket.recv(1024)
  message = pickle.loads(msg)
  return message

def stopMinerWork():
  global transactions
  global block
  global thread2
  
  transactions = []
  block = None
  thread2.stopThread()
  thread2 = ThreadMinerWork(transactions, block)

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def main():
  if len(sys.argv) != 3:
    print("Il faut mettre une adresse Ip et un port")
    sys.exit(1)

  else:
    miner(sys.argv[1],int(sys.argv[2]))

if __name__ == '__main__':
  thread1 = None
  thread2 = None
  previousBlock = None
  merkleRoot = None
  block = None
  transactions = None
  main()