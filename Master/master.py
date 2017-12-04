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
        msg = relay.recv(1024)
        msg = msg.decode()
        print("Reçu : {}".format(msg))
        relay.send(b"Ok")


if __name__ == '__main__':
  hote = ''
  port = 12800
  monMaster = Master(hote,port)