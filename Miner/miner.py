import sys
import socket
import select

class Miner:

  def __init__(self, hostName, hostPort):

    self.connectionToRelay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectionToRelay.connect((hostName, hostPort))
    print("Connection established with Relay on port {}".format(hostPort))

    self.encodeAndSend(self.connectionToRelay, "1") #s'identifie au relay en tant que miner

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

      msg = self.receiveAndDecode(self.connectionToRelay)
      print("Transaction : {}".format(msg))

      msg = "["+msg+"]"
      print("Bloc -> {}".format(msg))
      self.encodeAndSend(self.connectionToRelay, msg)

      
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

  def encodeAndSend(self, toSocket, message):
    msg = message.encode()
    toSocket.send(msg)

  def receiveAndDecode(self, fromSocket):
    msg = fromSocket.recv(1024)
    message = msg.decode()
    return message


def main():
  if len(sys.argv) != 3:
    print("Il faut mettre une adresse Ip et un port")
    sys.exit(1)

  else:
    monRelay = Miner(sys.argv[1],int(sys.argv[2]))

if __name__ == '__main__':
  main()