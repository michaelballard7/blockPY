from functools import reduce
import hashlib as hl
import json
import pickle

from utilities.hash_util import hash_block
from utilities.verification import Verification
# Import two functions from our hash_util.py file. Omit the ".py" in the import
from block import Block
from transaction import Transaction
from wallet import Wallet
# set the global mining reward
MINING_REWARD = 10

class Blockchain:
    """The Blockchain class manages the chain of blocks as well as open transactions and the node on which it's running.
    
    Attributes:
        :chain: The list of blocks
        :open_transactions (private): The list of open transactions
        :hosting_node: The connected node (which runs the blockchain).
    """

    def __init__(self, hosting_node_id):
        """The constructor of the Blockchain class."""
        # the genisis block is the founding block of my blockchain
        genesis_block = Block(0, '', [], 100, 0) # creates the genesis block as an object
        # initializing an empty blockchain as private attribute
        self.chain = [genesis_block]
        # unhandled transactions as a private attribute
        self.__open_transactions = []
        # excute load data at initializion
        self.load_data()
        # pass the hosting node to the block initiailization
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self,val):
        self.__chain = val

        
    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        """ Intitalize blockchain + open transactions from a data file """
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                # convert the loaded data because transactions should use an OrderedDict inorder not to manipulate data
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp']) # this now creates a block object
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                # convert the loaded data for the open transactions to also use the OrderedDict
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'],tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions

        except (IOError, IndexError):
            pass
        finally:
            print(" ")
            print(" ") 
            print('Welcome to WealthCoin!')
            print(" ")
            print(" ")


    def save_data(self):
        """Save blockchain + open transactions snapshot to a file """
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [ Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions] ,block_el.proof, block_el.timestamp ) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
        except IOError:
            print("Saving Failed")


    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0 
        # Try different PoW numbers and return the first valid one
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        """ Create a function to retrieve a users balance """
        participant = self.hosting_node
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of transactions that were already included in blocks of the blockchain
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of open transactions (to avoid double spending)
        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        # print(tx_sender)
        """ Replaced by one liner below using lambda and reduce """
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                             if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        """ Replaced by another one liner below using lambda and reduce again """
        amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                 if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        return amount_recieved - amount_sent


    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.
        Arguments:
            :sender: The sender of the funds.
            :recipient: The recipient of the funds.
            :amount: The amount of funds sent with the transaction (default = 1.0)
        """
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            # add new transaction details to open transactions 
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False


    def mine_block(self):
        """Create a new block and add open transactions to it."""
        if self.hosting_node == None:
            return False
        # grab the the last hashed block
        last_block = self.__chain[-1]
        # hash the last block inorder to use it in the stored hash value
        hashed_block = hash_block(last_block)  # pass in the last block to hash it and set to be passed to newly mined block
        proof = self.proof_of_work()
        reward_transaction = Transaction('Mining', self.hosting_node,'', MINING_REWARD)
        # Copy transaction instead of manipulating the original open_transactions list
        # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
        # create a shallow copy of the open transactions
        copied_transactions = self.__open_transactions[:]
        # verify all transactions during mining
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return False
        # append the mining reward transaction to all current open txns
        copied_transactions.append(reward_transaction)
        # create the new block object 
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        #append new block to the blockchain
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True



    def display_block(self):
        pass

