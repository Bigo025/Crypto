import hashlib

class Block:
	def __init__(self, size, previousBlockHash, merkleRoot, time, difficulty, nonce, transactionCounter, transactions):
		self.size = size
		self.previousBlockHash = previousBlockHash
		self.merkleRoot = merkleRoot
		self.time = time
		self.difficulty = difficulty
		self.nonce = nonce
		self.transactionCounter = transactionCounter
		self.transactions = transactions
		self.hash = self.hash_block()
		
	def hash_block(self):
	'''
	this function should not be like that it sould sent all infos to the miner and voila 
	'''
		sha = hashlib.sha256()
		sha.update(str(self.size) + 
					str(self.previousBlockHash) +
					str(self.merkleRoot) +
					str(self.time) +
					str(self.difficulty) +
					str(self.nonce) +
					str(self.transactionCounter) +
					str(self.transactions).encode())
		return sha.hexdigest()
