import hashlib

class Block:
  def __init__(self, previousBlockHash, merkleRoot, time, difficulty, nonce, transactions, blockHash = None):
    self.size = 8
    self.previousBlockHash = previousBlockHash
    self.merkleRoot = merkleRoot
    self.time = time
    self.difficulty = difficulty
    self.nonce = nonce
    self.transactions = transactions
    self.transactionCounter = len(self.transactions)
    self.hash = blockHash
    
  def hash_block(self):
    '''
    function used for tests
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
    self.hash = str(double_sha.digest())
    return self.hash

  def toString(self, log = False):
    if log:
      separator = "\n"
    else:
      separator = "&"
    res = ""
    res += str(self.size) + separator
    res += str(self.previousBlockHash) + separator
    res += str(self.merkleRoot) + separator
    res += str(self.time) + separator
    res += str(self.difficulty) + separator
    res += str(self.nonce) + separator
    res += str(self.transactionCounter) + separator
    res += str(self.transactions) + separator
    res += str(self.hash)
    if log:
      res += separator
    return res

    

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

  def setHash(string):
    self.hash = string
    
