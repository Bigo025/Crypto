from datetime import datetime
from Blocks import Block
import hashlib

blockchain = [] 


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
	
	
	
	
	
	