import sys
import socket
import select

class Relay:


  def __init__(self, hostName, portMaster, portRelay):
    #Connexion en client sur le master
    self.connectionToMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectionToMaster.connect((hostName, portMaster))
    print("Connection established with master on port {}".format(portMaster))

    #Serveur du relay
    self.relayServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.relayServer.bind((hostName, portRelay))
    self.relayServer.listen(5)
    print("Relay listen on port {}".format(portRelay))

    self.connectedWallets = []
    self.connectedMiners = []

    self.listenAll()


  def listenAll(self):
    serverStart = True

    while serverStart:

      self.listenToMaster()

      self.listenToNewConnections()
      
      self.listenToWallets()

      self.listenToMiners()


  def listenToMaster(self):
    messageFromMaster, wlist, xlist = select.select([self.connectionToMaster],
        [], [], 0.05)
    if len(messageFromMaster) != 0:
      msg = self.receiveAndDecode(self.connectionToMaster)
      print("Reçu Master: {}".format(msg))

      for wallet in self.connectedWallets :
        self.encodeAndSend(wallet, msg)


  def listenToNewConnections(self):
    #Ecoute si il y a de nouvelles connexions
    pendingConnections, wlist, xlist = select.select([self.relayServer],
      [], [], 0.05)
      
    #Ajoute les nouvelles connexions
    for connection in pendingConnections:
      clientConnection, connectionInfos = connection.accept()

      clientId = clientConnection.recv(1024)
      clientId = clientId.decode()
      if clientId == "0" :
        self.connectedWallets.append(clientConnection)
        print("Add new wallet")
      else :
        self.connectedMiners.append(clientConnection)
        print("Add new miner")


  def listenToWallets(self):

    #Ecoute si il y a des messages provenant de wallet 
    #Exceptions si il n'y a pas encore de relay connecté      
    try:
      walletsToRead, wlist, xlist = select.select(self.connectedWallets,
        [], [], 0.05)
    except select.error:
      pass
    else:
      for wallet in walletsToRead:
        msg = self.receiveAndDecode(wallet)
        print("Reçu Wallet: {}".format(msg))

        for miner in self.connectedMiners : 
          self.encodeAndSend(miner, msg)


  def listenToMiners(self):

    #Ecoute si il y a des messages provenant de wallet 
    #Exceptions si il n'y a pas encore de relay connecté      
    try:
      minersToRead, wlist, xlist = select.select(self.connectedMiners,
        [], [], 0.05)
    except select.error:
      pass
    else:
      for miner in minersToRead:
        msg = self.receiveAndDecode(miner)
        print("Reçu Miner: {}".format(msg))
        self.encodeAndSend(self.connectionToMaster, msg)

  def sendToMaster(self, message):
    self.connectionToMaster.send(message)


  def sendToMiners(self, message):
    pass


  def sendToWallets(self, message):
    pass

  def encodeAndSend(self, toSocket, message):
    msg = message.encode()
    toSocket.send(msg)

  def receiveAndDecode(self, fromSocket):
    msg = fromSocket.recv(1024)
    message = msg.decode()
    return message


def main():
  
  if len(sys.argv) != 4:
    print("Il faut mettre une adresse Ip , le port en client et le port en serveur")
    sys.exit(1)

  else:
    monRelay = Relay(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))

if __name__ == '__main__':
  main()