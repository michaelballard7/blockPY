import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """ Create a function to hash information """
    # return '-'.join([str(block[key]) for key in block])
    return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest() # hexDigest allows me to get a valid string
