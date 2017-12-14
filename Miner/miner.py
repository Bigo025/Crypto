import sys
import socket
import select
import hashlib
import struct
import codecs
import time
from datetime import datetime
import random
from threading import Thread
import pickle
from Crypto.Hash import SHA256
import binascii

from os import path
sys.path.append(path.abspath('../Utils'))
from Blocks import Block

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadMinerListenRelay(Thread):

  def __init__(self, relaySocket):
    global transactions
    Thread.__init__(self)
    self.connectionToRelay = relaySocket
    self.stop = False 

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    
    global previousBlock
    global transactions
    
    while(not self.stop):

      msg = receiveAndDecode(self.connectionToRelay)
      

      if (msg == "Stop") : #Message pour stop car un block a été trouvé par quelqu'un
        stopMinerWork(self.connectionToRelay)
        print(" Stop working")
      
      elif (msg[0] == "x") :
        previousBlock = msg[1]
        print(" New block received")
      
      elif (msg[0] == "t") : #C'est une transaction
        print(" Transaction received")
        transactions.append(msg[1])
        
        
  def stopThread(self):
    self.stop = True


#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadMinerWork(Thread):

  def __init__(self, rlayConnection):
    global transactions
    Thread.__init__(self)
    self.rlayConnection = rlayConnection
    self.stop = False

  def run(self):
    global transactions
    found = False
    nonce = random.randint(0, 1000000000)
    global previousBlock
    prev_block = previousBlock
    difficulty = 4
    while (not found and not self.stop):
      transactionsList = transactions[:]
      prev_block = previousBlock
      if (len(transactionsList) != 0): 

        mrklroot = self.calculateMerkleRoot(transactionsList)
        date = int(time.time())
        actual_date = datetime.now()
        bits = 0x1fffffff
        # https://en.bitcoin.it/wiki/Difficulty
        # Difficulté établie à 4 zéros
        exp = bits >> 24
        mant = bits & 0x3fff
        target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
        target_str = codecs.decode(target_hexstr, 'hex')

        header = ( codecs.decode(prev_block, 'hex') +
                  codecs.decode(mrklroot, 'hex') + struct.pack("<LLL", date, bits, nonce))
        hashtest = hashlib.sha256(hashlib.sha256(header).digest()).digest()
        hash = hashlib.sha256(hashlib.sha256(header).digest()).hexdigest()

        if ((hashtest[::-1] < target_str) and self.previousBlockStillTheSame(prev_block) and self.merkleRootStillTheSame(mrklroot) and not self.stop):
          print('success')
          found = True
          newBlock = Block(prev_block, mrklroot, actual_date, difficulty, nonce, transactionsList, hash[::-1])
          encodeAndSend(self.rlayConnection ,newBlock)
        nonce += 1
        if nonce==1000000000:
          nonce=0


  def merkleRootStillTheSame(self, currentMerkleRoot):
    global transactions
    transactionsList = transactions[:]
    newMerkleRoot = self.calculateMerkleRoot(transactionsList)
    return newMerkleRoot == currentMerkleRoot

  def calculateMerkleRoot(self, transactionsList):
    tmpTransactionsList = transactionsList
    newTransactionsList = []
    
    for i in range(0, len(tmpTransactionsList), 2):
      leftTransaction = str(tmpTransactionsList[i][0]) + str(tmpTransactionsList[i][1]) + str(tmpTransactionsList[i][2])+ str(tmpTransactionsList[i][3])
      if (i+1 != len(tmpTransactionsList)):
        rightTransaction = str(tmpTransactionsList[i+1][0]) + str(tmpTransactionsList[i+1][1]) + str(tmpTransactionsList[i+1][2])+ str(tmpTransactionsList[i+1][3])
      else:
        rightTransaction = ""
        
      # hash
      
      hashLeftTransaction = SHA256.new(leftTransaction.encode())
      if rightTransaction != "":
        hashRightTransaction = SHA256.new(rightTransaction.encode())
      
      if rightTransaction != "":
        newTransactionsList.append(hashLeftTransaction.hexdigest() + hashRightTransaction.hexdigest())
      else:
        newTransactionsList.append(hashLeftTransaction.hexdigest())
    transactionsList = newTransactionsList

    if len(tmpTransactionsList) > 1:
      self.calculateMerkleRoot(transactionsList)
    res = transactionsList[-1]

    return res

  def previousBlockStillTheSame(self, currentPreviousBlock):
      global previousBlock
      return currentPreviousBlock == previousBlock
  
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
  global transactions
  global previousBlock

  transactions = receiveAndDecode(connectionToRelay)
  previousBlock = receiveAndDecode(connectionToRelay)

  thread1 = ThreadMinerListenRelay(connectionToRelay)
  thread2 = ThreadMinerWork(connectionToRelay)
  
  thread1.start()
  thread2.start()

def encodeAndSend(toSocket, message):
  msg = pickle.dumps(message)
  toSocket.send(msg)

def receiveAndDecode(fromSocket):
  msg = fromSocket.recv(4096)
  message = pickle.loads(msg)
  return message

def stopMinerWork(relaySocket):
  global transactions
  global thread2
  
  transactions = []
  thread2.stopThread()
  thread2 = ThreadMinerWork(relaySocket)
  thread2.start()

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
  transactions = None
  main()
