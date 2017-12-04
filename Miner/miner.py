import socket
import select

class Miner:

  def __init__(self, hostName, hostPort):

    self.connectionToRelay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectionToRelay.connect((hostName, hostPort))
    print("Connection established with Relay on port {}".format(hostPort))

    self.connectionToRelay.send(b"1") #s'identifie au relay en tant que miner

    self.bloc = None
    self.listenToRelay()

  def listenToRelay(self):
    while(True):
      #newTransaction = self.connectionToRelay.recv(1024) #1024 = nbre caractere max du msg
      #if newTransaction[0] == 0 :
        #if self.transactionIsValid(newTransaction):
          #self.addToBlock()

        #if self.blockIsReady():
          #self.sendMinedBlock()

      #if newTransaction[0] == 1 :
        #add bitcoins

      msg = input("> ")
      msg = msg.encode()
      self.connectionToRelay.send(msg)

      msg = self.connectionToRelay.recv(4096)
      msg = msg.decode()
      print(msg)

  def transactionIsValid(self, transaction):
    isValid = False
    #...Code...

    return isValid

  def addToBlock(self):
    if self.bloc == None :
      pass
      #Create block 
    #...Code...

  def blockIsReady(self):
    isReady = False
    #...Code...

    return isReady

  def sendMinedBlock(self):
    #...Code...
    self.relay_connection.send("block")

    self.block = None


if __name__ == '__main__':
  hoteClient = "localhost"
  portClient = 8888
  monRelay = Miner(hoteClient,portClient)