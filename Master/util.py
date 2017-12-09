from datetime import datetime
from Blocks import Block
import re #regex
import hashlib

blockchain = []
currentBlock = None
separator = "-------------------------------------"
numberOfBlockAttributes = 9

def block_to_text(block):
        txt = ""
        txt += str(block.getSize()) + "\n"
        txt += str(block.getPreviousBlockHash()) + "\n"
        txt += str(block.getMerkleRoot()) + "\n"
        txt += str(block.getTime()) + "\n"
        txt += str(block.getDifficulty()) + "\n"
        txt += str(block.getNonce()) + "\n"
        txt += str(block.getTransactionCounter()) + "\n"
        txt += str(block.getTransactions()) + "\n"
        txt += str(block.getHash()) + "\n"
        return txt
        
        
def add_block_to_log():
        file = open("blockchain.log","a")
        file.write(separator+"\n")
        file.write(block_to_text(currentBlock))
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

currentBlock = genesis_block()
add_block_to_log()
import_previous_block()
	
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
	return res
	
	
	
	
	
	
