import sys
import socket
import select

class Master:


  def __init__(self, hostName, hostPort):
    #Serveur du master
    self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.main_connection.bind((hostName, hostPort))
    self.main_connection.listen(5)
    print("Master listen on port {}".format(hostPort))

    self.connectedRelays = []

    self.listenAll()

  def listenAll(self):
    serverStart = True

    while serverStart:
      
      self.listenToNewConnections()

      self.listenToRelay()

  def listenToNewConnections(self):
    #Ecoute si il y a de nouvelles connexions
    pendingConnections, wlist, xlist = select.select([self.main_connection],
        [], [], 0.05)
      
    #Ajoute les nouvelles connexions
    for connection in pendingConnections:
      relayConnection, connectionInfos = connection.accept()
      self.connectedRelays.append(relayConnection)
      print("New relay")

  def listenToRelay(self):
    #Ecoute si il y a des messages provenant de relay 
    #Exceptions si il n'y a pas encore de relay connecté      
    try:
      relaysToRead, wlist, xlist = select.select(self.connectedRelays,
        [], [], 0.05)
    except select.error:
      pass
    else:
      for relay in relaysToRead:
        msg = self.receiveAndDecode(relay)
        print("Reçu : {}".format(msg))
        msg = "-" + msg + "-"
        print("Bloc validé : {}".format(msg))
        self.encodeAndSend(relay, msg)

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
    monMaster = Master(sys.argv[1],int(sys.argv[2]))

if __name__ == '__main__':
  main()