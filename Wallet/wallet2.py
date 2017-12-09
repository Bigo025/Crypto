"""Imports."""
from Crypto.PublicKey import DSA
from Crypto.Cipher import AES
from Crypto.Random import random
from Crytodome.PublicKey import RSA
import codecs
import json
import pickle
import requests
import Block
import CryptoLib


class Wallet:
    """Class for the users' wallets."""

    def __init__(self, relayPort, myPassword):
        """Init."""
       
        myDSAKeys = DSA.generate(1024)
        
        self.secret_code = myPassword
        self.myRSAPublicKey = key.publickey().exportkey()
        self.myRSAPrivate_key = key.exportkey()
        self.myAddress = CryptoLib.getAddressFromPublicKey(self.myRSAPublicKey.y) 
        self.unspentTxs = [] # list of blocks with money I can spend (Blocks with transactions that reciever is me)
        self.relayPort = relayPort  #Port d'ecout relay
        self.relayIP = "http://localhost:" + str(self.relayPort) # Creation adresse relay
        self.BlockChain = []


    def howMuchMoneyDoIHave(self): #mise a jour du portefeuile
        """Determine how much money the user associated with the wallet has."""
        self.unspentTxs=self.UpdateUnspentTxs() 
        moneyAvailable = 0
        for tx in self.unspentTxs: #parcours la liste des transactions
            if tx.receiver==self.myAddress:  #verifie le benificaire de la transaction
                moneyAvailable = moneyAvailable + tx.amount # ajourne le solde
        print("Current balance: " + str(moneyAvailable))
        return moneyAvailable

    def CreateTransaction(self, ReceiverAddress, amount, myPassword):
        """Creer nouvelle transaction"""
       



    def spentMyMoney(self, ReceiverAddress, amount, myPassword):
        balance=self.howMuchMoneyDoIHave()
        if amount<balance:
            newTransaction=self.CreateTransaction(ReceiverAddress, amount, myPassword)
            self.sendTxToRelay(newTransaction)
        else:
            print("Votre solde est insuffisant")

    def getmyAddress(self):
        return self.myAddress


    def UpdateUnspentTxs(self):    
        """mise a jour des transaction non receptionnées utilisées pour actualiser son portefeuille"""
        req = requests.get(self.relayIP + "/UnspentTx")  # requete 'get' de "UnspentTx" au Relay :   UnspentTx = liste des transactions de la blockchain
        unspentTxs = pickle.loads(req.content)  
        self.unspentTxs = unspentTxs
        return unspentTxs

    def sendTxToRelay(self,tx):
        """Send new transaction to the linked relay."""
        pickledBlock = codecs.encode(pickle.dumps(tx), "base64").decode()
        jsonForm=json.dumps(pickledBlock)
        requests.post(self.relayIP + "/TxToRelay", json=jsonForm)

    def reqBalance(self,publicKey):
        pickledKey = codecs.encode(pickle.dumps(publicKey), "base64").decode()
        jsonForm=json.dumps(pickledKey)
        req=requests.post(self.relayIP + "/BalanceRequest",json=jsonForm)
        return int(req.content)


    def requestBlockChain(self):
        """Get the whole blockchain from the relay."""
        req = requests.get(self.relayIP + "/Blockchain")
        blockChain = pickle.loads(req.content)
        self.BlockChain = blockChain
        return blockChain
    
    def minerTransaction(self,amount,myPassword):
        initialTransaction=self.CreateTransaction(self.myAddress,amount,myPassword)
        return initialTransaction
