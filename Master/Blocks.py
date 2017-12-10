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
    double_sha = hashlib.sha256()
    data = str(self.size) + \
	  str(self.previousBlockHash) +\
      str(self.merkleRoot) +\
      str(self.time) +\
      str(self.difficulty) +\
      str(self.nonce) +\
      str(self.transactionCounter) +\
      str(self.transactions)
  sha.update(data.encode())
  double_sha.update(sha.digest())
  return double_sha.digest()

    

  def getSize(self):
    return self.size
  def getPreviousBlockHash(self):
    return self.previousBlockHash
  def getMerkleRoot(self):
    return self.merkleRoot
  def getTime(self):
    return self.time
  def getDifficulty(self):
    return self.difficulty
  def getNonce(self):
    return self.nonce
  def getTransactionCounter(self):
    return self.transactionCounter
  def getTransactions(self):
    return self.transactions
  def getHash(self):
    return self.hash
    
