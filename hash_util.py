import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """ Create a function to hash information """
    # create a dictionary copy of my block object inorder to convert to JSON
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hl.sha256(json.dumps(hashable_block, sort_keys=True).encode()).hexdigest() # hexDigest allows me to get a valid string
