import sys
import socket
import select
from threading import Thread

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenMaster(Thread):

  def __init__(self, masterSocket, wallets):
    Thread.__init__(self)
    self.connectionToMaster = masterSocket
    self.connectedWallets = wallets

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while True :
      messageFromMaster, wlist, xlist = select.select([self.connectionToMaster],
        [], [], 0.05)
      if len(messageFromMaster) != 0:
        msg = receiveAndDecode(self.connectionToMaster)
        print("Reçu Master: {}".format(msg))

        for wallet in self.connectedWallets :
          encodeAndSend(wallet, msg)

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenToNewConnections(Thread):

  def __init__(self, serverSocket, wallets, miners):
    Thread.__init__(self)
    self.relayServer = serverSocket
    self.connectedWallets = wallets
    self.connectedMiners = miners

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

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
          print("Add new miner")
      

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenWallets(Thread):

  def __init__(self, wallets, miners):
    Thread.__init__(self)
    self.connectedWallets = wallets
    self.connectedMiners = miners

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
          print("Reçu Wallet: {}".format(msg))

          for miner in self.connectedMiners : 
            encodeAndSend(miner, msg)
      

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadRelayListenMiners(Thread):

  def __init__(self, masterSocket, miners):
    Thread.__init__(self)
    self.connectionToMaster = masterSocket
    self.connectedMiners = miners

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
          msg = receiveAndDecode(miner)
          print("Reçu Miner: {}".format(msg))
          encodeAndSend(self.connectionToMaster, msg)
      

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

  connectedWallets = []
  connectedMiners = []

  thread1 = ThreadRelayListenMaster(connectionToMaster, connectedWallets)
  thread2 = ThreadRelayListenToNewConnections(relayServer, connectedWallets, connectedMiners)
  thread3 = ThreadRelayListenWallets(connectedWallets, connectedMiners)
  thread4 = ThreadRelayListenMiners(connectionToMaster, connectedMiners)

  thread1.start()
  thread2.start()
  thread3.start()
  thread4.start()


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


def main():
  
  if len(sys.argv) != 4:
    print("Il faut mettre une adresse Ip , le port en client et le port en serveur")
    sys.exit(1)

  else:
    relay(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))

if __name__ == '__main__':
  main()