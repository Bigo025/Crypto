import sys
import socket
import select
from os import path
sys.path.append(path.abspath('../Utils'))
from util import *
from threading import Thread
import pickle

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

class ThreadMasterListenToNewConnexion(Thread):

  def __init__(self, masterSocket, relays):

    Thread.__init__(self)
    self.main_connection = masterSocket
    self.connectedRelays = relays


  def run(self):
    """Code à exécuter pendant l'exécution du thread."""

    while True :
      #Ecoute si il y a de nouvelles connexions

      pendingConnections, wlist, xlist = select.select([self.main_connection],
        [], [], 0.05)

      #Ajoute les nouvelles connexions
      for connection in pendingConnections:
        relayConnection, connectionInfos = connection.accept()
        self.connectedRelays.append(relayConnection)
        print("New relay")
        global previousBlock
        encodeAndSend(relayConnection, previousBlock)



#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------
#Select peut etre remplacé par rcv pou recupérer le premier arrivé MAIS il y a peut etre 
#conflit avec l'autre thread des new connection
# Alors Soit on garde Select et o nregarde la date de reception
# Ou on rcv mais alors on enleve les thread, et on reunis les deux en une boucle true


class ThreadMasterListenToRelay(Thread):

  def __init__(self, relays):
    Thread.__init__(self)
    self.connectedRelays = relays

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    global previousBlock

    #Ecoute si il y a de nouvelles connexions

    while True :
      try:
        relaysToRead, wlist, xlist = select.select(self.connectedRelays,
          [], [], 0.05)
      except select.error:
        pass
      else:
        for relay in relaysToRead:
          msg = receiveAndDecode(relay)
          newBlock = msg
          if (newBlock == None):
            print("Error: creation block from string")
          else:
            if (validate_block(newBlock, previousBlock)):
              print("Bloc validé")
              previousBlock = newBlock
              add_block_to_log(newBlock)
              for relayToSend in self.connectedRelays:
                encodeAndSend(relayToSend, newBlock)


#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------


def master(hostName, hostPort):
  #Serveur du master
  main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  main_connection.bind((hostName, hostPort))
  main_connection.listen(5)
  print("Master listen on port {}".format(hostPort))

  connectedRelays = []
      
  thread1 = ThreadMasterListenToNewConnexion(main_connection, connectedRelays)
  thread2 = ThreadMasterListenToRelay(connectedRelays)

  thread1.start()
  thread2.start()


def encodeAndSend(toSocket, message):
  msg = pickle.dumps(message)
  toSocket.send(msg)

def receiveAndDecode(fromSocket):
  msg = fromSocket.recv(10000)
  message = pickle.loads(msg)
  return message

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------

def main():
  
  if len(sys.argv) != 3:
    print("Il faut mettre une adresse Ip et un port")
    sys.exit(1)

  else:
    master(sys.argv[1],int(sys.argv[2]))

if __name__ == '__main__':
  previousBlock = genesis_block()
  file = open("../Utils/blockchain.log","w")
  file.write("")
  file.close()
  add_block_to_log(previousBlock)
  main()
