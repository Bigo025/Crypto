from datetime import datetime
from Blocks import Block
import re #regex
import hashlib

blockchain = []
currentBlock = None
separator = "-------------------------------------"
numberOfBlockAttributes = 9

        
def add_block_to_log():
  file = open("blockchain.log","a")
  file.write(separator+"\n")
  file.write(toString(currentBlock, True))
  file.close()

        
def import_previous_block():
  file = open("blockchain.log","r")
  linesList = file.read().splitlines()
  attributeIndex = 0
  for line in linesList:
    if line == separator:
      attributeIndex = 0
    elif attributeIndex == 1:
      blockSize = int(line)
    elif attributeIndex == 2:
      previousBlockHash = line
    elif attributeIndex == 3:
      merkleRoot = line
    elif attributeIndex == 4:
      blockTime = datetime.strptime(line,'%Y-%m-%d %H:%M:%S.%f')
    elif attributeIndex == 5:
      difficulty = int(line)
    elif attributeIndex == 6:
      nonce = int(line)
    elif attributeIndex == 7:
      transactionsCounter = int(line)
    elif attributeIndex == 8:
      data = line
      transactions = []
      data = re.split("\W+",data)
      while '' in data:
        data.remove('')
      for transaction in data:
        transactions.append(transaction)
    elif attributeIndex == 9:
      blockHash = line
    elif attributeIndex > numberOfBlockAttributes:
      print("error in numberOfBlockAttributes")
      attributeIndex+=1
  file.close()


def genesis_block():
  '''
  create the first bock manually => the genesis block
  '''
  # example
  genesis = Block(285,
                  None,
                  "1dee35fe304db59e2d0b3e0d19bb43454dc8a8bca95ac8da6570763f45ddf3d5",
                  datetime.now(),
                  1,
                  100,
                  0,
                  ["1dee35fe304db59e2d0b3e0d19bb43454dc8a8bca95ac8da6570763f45ddf3d5"])
  return genesis

	
def hash_transaction(transaction):
  # ptt que ce que je fais n'est pas correcte  !
  #transaction form : [sender, receiver, datetime.now(), amount]
  data = str(transaction[0]) + str(transaction[1]) + str(transaction[2]) + str(transaction[3])
  sha = hashlib.sha256(data.encode())
  double_sha = hashlib.sha256(sha.digest())
  return double_sha.digest()
		

# merkleroot : create a new merkle tree and insert the root 
# transactions is a list of hashed transactions not hashed blocks !
def new_block(size, previousblockhash, merkleroot, difficulty, nonce, transactionCounter, transactions):
  newBlock = Block(size, previousblockhash, merkleroot, datetime.now(), difficulty, nonce, transactionCounter +1, transactions)
  return newBlock

def new_block_from_list(attributesList):
  if len(attributesList) == 9:
    blockSize = int(attributesList[0])
    previousBlockHash = attributesList[1]
    merkleRoot = attributesList[2]
    blockTime = datetime.strptime(attributesList[3],'%Y-%m-%d %H:%M:%S.%f')
    difficulty = int(attributesList[4])
    nonce = int(attributesList[5])
    transactionsCounter = int(attributesList[6])

    data = attributesList[7]
    transactions = []
    data = re.split("\W+",data)
    while '' in data:
      data.remove('')
    for transaction in data:
      transactions.append(transaction)

    blockHash = attributesList[8] # recalculated when creating block object
    return Block(blockSize, previousBlockHash, merkleRoot, blockTime, difficulty, nonce, transactionsCounter, transactions)
  else:
    print("util.py -> new_block_from_list: wrong number of attributes")

def new_block_from_string(string):
  attributesList = string.split("&") #separator = &
  return new_block_from_list(attributesList)
	
# blockchain.append(genesis_block())
# blockchain.append(new_block(size, ...))


def validate_block(newBlock, previousblock):
  res = True
  if (previousblock.getTransactionCounter()+1 != newBlock.getTransactionCounter):
    print("Invalid transactionCounter")
    res = False
  elif (previousblock.getHash() != newBlock.getPreviousBlockHash):
    print("Invalid previousBlockHash")
    res = False
  elif (newBlock.getHash())[:newBlock.getDifficulty()] != newBlock.getDifficulty()*"0":
    print("Invalid difficulty")
    res = False
  return res
