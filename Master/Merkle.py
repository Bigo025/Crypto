import hashlib
from collections import OrderedDict

class MerkleTree:
  def __init__(self, transactionsList):
    self.transactionsList = transactionsList
    self.previousTransaction = OrderedDict()
    if (len(self.transactionsList) > 1):
    
    def build_tree(self):
    tempTransactionsList = self.transactionsList
    tempPreviousTransaction = self.previousTransaction
    newTransactionsList = []
    
    for i in range(0, len(tempTransactionsList), 2):
      leftTransaction = tempTransactionsList[i]
      # If there is still any elements on the right 
      if (i+1 != len(tempTransactionsList)):
        rightTransaction = tempTransactionsList[i+1]
        
      else:
        rightTransaction = ""
      
      # hash
      hashLeftTransaction = hashlib.sha256(leftTransaction.encode())
      
      if  rightTransaction != "":
        hashRightTransaction = hashlib.sha256(RightTransaction.encode())
        
      # add the Transaction hash to the dictionary 
      tempPreviousTransaction[tempTransactionsList[i]] = hashLeftTransaction.hexdigest()
      if rightTransaction != "":
        tempPreviousTransaction[tempTransactionsList[i+1]] = hashRightTransaction.hexdigest()
      
      # fill newTransactionsList
      if  rightTransaction != "":
        newTransactionsList.append(hashLeftTransaction.hexdigest() + hashRightTransaction.hexdigest())
        
      else:
        newTransactionsList.append(hashLeftTransaction.hexdigest())
    
    if (len(tempTransactionsList) != 1):
      self.transactionsList = newTransactionsList
      self.previousTransaction = tempPreviousTransaction
      
      # recursive function 
      self.build_tree()
  
  def getPreviousTransaction(self):
    return self.previousTransaction
    
  def getMerkelRoot(self):
    return(self.previousTransaction[self.previousTransaction.keys()[-1]])
      
    
  