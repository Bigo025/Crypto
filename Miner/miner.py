import sys
import socket
import select
from threading import Thread

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadMinerListenRelay(Thread):

  def __init__(self, relaySocket):
    Thread.__init__(self)
    self.connectionToRelay = relaySocket

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while(True):

      msg = receiveAndDecode(self.connectionToRelay)
      print("Transaction : {}".format(msg))

      msg = "["+msg+"]"
      print("Bloc -> {}".format(msg))
      encodeAndSend(self.connectionToRelay, msg)

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadMinerWork(Thread):

  def __init__(self):
    Thread.__init__(self)

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while(True):
      break

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def miner (hostName, hostPort):

  connectionToRelay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connectionToRelay.connect((hostName, hostPort))
  print("Connection established with Relay on port {}".format(hostPort))

  encodeAndSend(connectionToRelay, "1") #s'identifie au relay en tant que miner

  bloc = None
  thread1 = ThreadMinerListenRelay(connectionToRelay)
  thread2 = ThreadMinerWork()
  
  thread1.start()
  thread2.start()


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
  if len(sys.argv) != 3:
    print("Il faut mettre une adresse Ip et un port")
    sys.exit(1)

  else:
    miner(sys.argv[1],int(sys.argv[2]))

if __name__ == '__main__':
  main()