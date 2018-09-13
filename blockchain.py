from functools import reduce
import hashlib as  hl
from collections import OrderedDict
from block import Block
import json
import pickle
from transaction import Transaction
from verification import Verification
from hash_util import hash_block, hash_string_256

# Initializing our (empty) blockchain list
blockchain = []
# unhandled transactions
open_transactions = []
# set the global mining reward
MINING_REWARD = 10
# establish the ownership of this blockchain node
owner = 'Michael'

def load_data():
    """ Intitalize blockchain + open transactions from a data file """
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            blockchain = json.loads(file_content[0][:-1])
            # convert the loaded data because transactions should use an OrderedDict inorder not to manipulate data
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp']) # this now creates a block object
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])

            # convert the loaded data for the open transactions to also use the OrderedDict
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions

    except (IOError, IndexError):
        print('File not found')
        """ Step:  intializing my blockchain list if file not found """
        # the genisis block is the founding block of my blockchain
        genesis_block = Block(0, '', [], 100, 0) # creates the genesis block as an object
        # initiate my blockchain and add the genisis block
        blockchain = [genesis_block]
        # create a variable to serve as a queue for unmined
        open_transactions = []
 
    finally: 
        print('Cleanup')


load_data() # execute the function as soon as I define it


def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            saveable_chain = [block.__dict__ for block in [ Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions] ,block_el.proof, block_el.timestamp ) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
    except IOError:
        print("Saving Failed")


def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0 

    verifier = Verification()

    # Try different PoW numbers and return the first valid one
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    """ Create a function to retrieve a users balance 
    
        Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    """ Replaced by one liner below using lambda and reduce """
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > tx_sum + 0 else 0, tx_sender ,0)
    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    """ Replaced by another one liner below using lambda and reduce again """
    amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    return amount_recieved - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.
    Arguments:
        :sender: The sender of the funds.
        :recipient: The recipient of the funds.
        :amount: The amount of funds sent with the transaction (default = 1.0)
    """
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        # add new transaction details to open transactions 
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    """Create a new block and add open transactions to it."""
    # grab the the last hashed block
    last_block = blockchain[-1]
    # hash the last block inorder to use it in the stored hash value
    hashed_block = hash_block(last_block)  # pass in the last block to hash it and set to be passed to newly mined block
    proof = proof_of_work()
    reward_transaction = Transaction('Mining', owner, MINING_REWARD)
    # Copy transaction instead of manipulating the original open_transactions list
    # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
    # create a shallow copy of the open transactions
    copied_transactions = open_transactions[:]
    # append the mining reward transaction to all current open txns
    copied_transactions.append(reward_transaction)
    # create the new block object 
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    #append new block to the blockchain
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print( " ")
        print(block)
        print(" ")
    else:
        print('-' * 20)

waiting_for_input = True

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    """ Create an infite loop to run the blockchain cli """
    # print the user options
    print(" ------------------------------------- ")
    print(" ")
    print('Please choose an option number?')
    print(" ")
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Check transaction validity')
    print('q: Quit')
    print(" ")
    print(" ------------------------------------- ")
    print(" ")

    # save user input
    user_choice = get_user_choice()

    # Create a conditions to service the user input
    if user_choice == '1':
        tx_data = get_transaction_value() 
        recipient, amount = tx_data # I can destructure or unpack a tuple as such
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount): # add transactiont to open transactions
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':  # output existing blocks
        print_blockchain_elements()
    elif user_choice == '4':
        verifier = Verification()
        if verifier.verify_transactions(open_transactions,get_balance):
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print(" ------------------------------------------------ ")
    print(" ")
    print('Current Balance of {}\'s Account:{:6.2f}'.format(owner, get_balance("Michael")))
    print(" ")
else:
    print('User left!')

print('Done!')