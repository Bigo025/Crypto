from datetime import datetime
from Blocks import Block

blockchain = [] 


def genesis_block():
	'''
	create the first bock manually => the genesis block
	'''
	# example 
	genesis = Block(285, 
			None, 
			"merkleroot hash",
			datetime.now(),
			1.000, 
			20832, 
			0, 
			["hash of the transactions in a list"])
	return genesis
		
	
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
	
	
	
	
	
	