import socket
import select

class Wallet:

  def __init__(self, hostName, hostPort):
  	#Connexion en client sur le master
    self.connectionToRelay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectionToRelay.connect((hostName, hostPort))
    print("Connection established with Relay on port {}".format(hostPort))

    self.connectionToRelay.send(b"0") #s'identifie au relay en tant que wallet

    self.listenToRelay()

  def listenToRelay(self):

    while True :

      msg = input("> ")
      msg = msg.encode()
      self.connectionToRelay.send(msg)

      msg = self.connectionToRelay.recv(4096)
      msg = msg.decode()
      print(msg)


if __name__ == '__main__':
  hoteClient = "localhost"
  portClient = 8888
  monRelay = Wallet(hoteClient,portClient)