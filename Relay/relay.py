import socket
import select

class Relay:


  def __init__(self, hostMaster, portMaster, hostRelay, portRelay):
    #Connexion en client sur le master
    self.connectionToMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectionToMaster.connect((hostMaster, portMaster))
    print("Connection established with master on port {}".format(portMaster))

    #Serveur du relay
    self.relayServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.relayServer.bind((hostRelay, portRelay))
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
      msg = self.connectionToMaster.recv(4096)
      msg = msg.decode()
      print("Reçu Master: {}".format(msg))


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
        msg = wallet.recv(1024)
        msg = msg.decode()
        print("Reçu Wallet: {}".format(msg))
        wallet.send(b"Ok")


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
        msg = miner.recv(1024)
        msg = msg.decode()
        print("Reçu Miner: {}".format(msg))
        miner.send(b"Ok")

  def sendToMaster(self, message):
    self.connectionToMaster.send(message)


  def sendToMiners(self, message):
    pass


  def sendToWallets(self, message):
    pass


if __name__ == '__main__':
  hoteClient = "localhost"
  portClient = 12800
  hoteServeur = ""
  portServeur = 8888
  monRelay = Relay(hoteClient,portClient,hoteServeur,portServeur)