import socket

class Miner:

	self.bitcoins = 0 #Bitcoins reward for mined block

	def __init__(self, hostName, hostPort):

		self.relay_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.relay_connection.connect((hostName, hostPort))

		self.bloc = None
		self.listenToRelay()


	def listenToRelay(self):
		while(True):
			newTransaction = self.relay_connection.recv(1024) #1024 = nbre caractere max du msg
			if newTransaction[0] == 0 :
				if self.transactionIsValid(newTransaction):
					self.addToBlock()

				if self.blockIsReady():
					self.sendMinedBlock()

			if newTransaction[0] == 1 :
				#add bitcoins

	def transactionIsValid(self, transaction):
		isValid = False
		#...Code...

		return isValid

	def addToBlock(self):
		if self.bloc == None :
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