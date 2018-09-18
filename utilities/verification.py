from utilities.hash_util import hash_block, hash_string_256
from wallet import Wallet


class Verification:

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

        Arguments:
            :transactions: The transactions of the block for which the proof is created.
            :last_hash: The previous block's hash which will be stored in the current block.
            :proof: The proof number we're testing.
        """
        # create a string with all the hash inputs

        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        # Hash the string
        # IMPORTANT: This is NOT the same hash as will be stored in the previous_hash. It's a not a block's hash. It's only used for the proof-of-work algorithm.
        guess_hash = hash_string_256(guess)
        # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
        # This condition is of course defined by you. You could also require 10 leading 0s - this would take significantly longer (and this allows you to control the speed at which new blocks can be added)
        # print(guess_hash)
        return guess_hash[0:2] == '00' #here Is where I can get fancy with my condition to check for a valid hash. Use academic research to guide me.


    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid, False otherwise."""
        # loop through each block and compare each available block
        for (index, block) in enumerate(blockchain): # Generate a destructured tuple with enumerate function
            if index == 0:
                continue # skip the validation of the genesis block
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False

            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False

        return True # return true to continue process if all blocks are valid


    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds = True):
        """ Verify that an sender has suffiecient funds """
        if check_funds:
            sender_balance = get_balance()
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """ One line implementation to validate that all transactions are true """
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])