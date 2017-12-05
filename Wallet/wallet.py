import sys
import socket
import select

class Wallet:

  def __init__(self, hostName, hostPort):
    #Connexion en client sur le master
    self.connectionToRelay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectionToRelay.connect((hostName, hostPort))
    print("Connection established with Relay on port {}".format(hostPort))

    self.encodeAndSend(self.connectionToRelay, "0") #s'identifie au relay en tant que wallet

    self.listenToRelay()

  def listenToRelay(self):

    while True :

      msg = input("> ")

      self.encodeAndSend(self.connectionToRelay, msg)

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
    monRelay = Wallet(sys.argv[1],int(sys.argv[2]))

if __name__ == '__main__':
  main()