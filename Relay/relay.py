import sys
import socket
import select
from threading import Thread
import pickle

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenMaster(Thread):

  def __init__(self, masterSocket, wallets, miners):
    Thread.__init__(self)
    self.connectionToMaster = masterSocket
    self.connectedWallets = wallets
    self.connectedMiners = miners

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    global lastBlock
    while True :
      messageFromMaster, wlist, xlist = select.select([self.connectionToMaster],
        [], [], 0.05)
      if len(messageFromMaster) != 0:
        lastBlock = receiveAndDecode(self.connectionToMaster)
        print("Reçu Master: {}".format(msg))

        for miner in self.connectedMiners :
          encodeAndSend(miner, ["x",lastBlock.getHash()])

        for wallet in self.connectedWallets :
          encodeAndSend(wallet, lastBlock)

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenToNewConnections(Thread):

  def __init__(self, serverSocket, wallets, miners, transactions):
    Thread.__init__(self)
    self.relayServer = serverSocket
    self.connectedWallets = wallets
    self.connectedMiners = miners
    self.transactionsList = transactions

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    global lastBlock

    while True :

      #Ecoute si il y a de nouvelles connexions
      pendingConnections, wlist, xlist = select.select([self.relayServer],
        [], [], 0.05)
        
      #Ajoute les nouvelles connexions
      for connection in pendingConnections:
        clientConnection, connectionInfos = connection.accept()

        clientId = receiveAndDecode(clientConnection)

        if clientId == "0" :
          self.connectedWallets.append(clientConnection)
          print("Add new wallet")
        else :
          self.connectedMiners.append(clientConnection)
          encodeAndSend(self.transactionsList) #Liste des transactions
          encodeAndSend(lastBlock) #LastBlock
          print("Add new miner")
      

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenWallets(Thread):

  def __init__(self, wallets, miners, transactions):
    Thread.__init__(self)
    self.connectedWallets = wallets
    self.connectedMiners = miners
    self.transactionsList = transactions

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while True :

      #Ecoute si il y a des messages provenant de wallet 
      #Exceptions si il n'y a pas encore de relay connecté      
      try:
        walletsToRead, wlist, xlist = select.select(self.connectedWallets,
          [], [], 0.05)
      except select.error:
        pass
      else:
        for wallet in walletsToRead:
          msg = receiveAndDecode(wallet)
          self.transactionsList.append(msg)
          print("Transaction received from Wallet")

          for miner in self.connectedMiners : 
            encodeAndSend(miner, ["t", msg])
      

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenMiners(Thread):

  def __init__(self, masterSocket, miners, transactions):
    Thread.__init__(self)
    self.connectionToMaster = masterSocket
    self.connectedMiners = miners
    self.transactionsList = transactions

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while True :

      #Ecoute si il y a des messages provenant de wallet 
      #Exceptions si il n'y a pas encore de relay connecté      
      try:
        minersToRead, wlist, xlist = select.select(self.connectedMiners,
          [], [], 0.05)
      except select.error:
        pass
      else:
        for miner in minersToRead:
          self.transactionsList = []
          msg = receiveAndDecode(miner)
          print("New block received from a Miner")
          encodeAndSend(self.connectionToMaster, msg)

        for miner in self.connectedMiners:
          encodeAndSend(miner, "Stop")
      

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------


def relay(hostName, portMaster, portRelay):

  #Connexion en client sur le master
  connectionToMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connectionToMaster.connect((hostName, portMaster))
  print("Connection established with master on port {}".format(portMaster))

  #Serveur du relay
  relayServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  relayServer.bind((hostName, portRelay))
  relayServer.listen(5)
  print("Relay listen on port {}".format(portRelay))

  global lastBlock

  lastBlock = receiveAndDecode(connectionToMaster)

  connectedWallets = []
  connectedMiners = []
  transactionsList = []

  thread1 = ThreadRelayListenMaster(connectionToMaster, connectedWallets, connectedMiners)
  thread2 = ThreadRelayListenToNewConnections(relayServer, connectedWallets, connectedMiners, transactionsList)
  thread3 = ThreadRelayListenWallets(connectedWallets, connectedMiners, transactionsList)
  thread4 = ThreadRelayListenMiners(connectionToMaster, connectedMiners, transactionsList)

  thread1.start()
  thread2.start()
  thread3.start()
  thread4.start()


def encodeAndSend(toSocket, message):
  msg = pickle.dumps(message)
  toSocket.send(msg)

def receiveAndDecode(fromSocket):
  msg = fromSocket.recv(4096)
  message = pickle.loads(msg)
  return message

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------


def main():
  
  if len(sys.argv) != 4:
    print("Il faut mettre une adresse Ip , le port en client et le port en serveur")
    sys.exit(1)

  else:
    relay(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))

if __name__ == '__main__':
  lastBlock = None
  main()