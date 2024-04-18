from hashlib import sha256

# Stringify and concatenate all arguments and produces a sha256 hash as a result
def updatehash(*args):
    hashing_text = ""; h = sha256()

    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

# The "block" of the blockchain. Points to the previous block by its unique hash in previous_hash.
class Block():
    def __init__(self,number=0, previous_hash="0"*64, data=None, nonce=0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    # Compute a sha256 hash for the block's data.
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce
        )

    # Returns a string of the block's data. Useful for diagnostic print statements.
    def __str__(self):
        return str("Block# : %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce
            )
        )


# A chain of the blocks.
class Blockchain():
    # the number of zeros in front of each hash
    difficulty = 4

    # restarts a new blockchain or the existing one upon initialization
    def __init__(self):
        self.chain = []

    # add a new block to the chain
    def add(self, block):
        self.chain.append(block)

    # remove a block from the chain
    def remove(self, block):
        self.chain.remove(block)

    # find the nonce of the block that satisfies the difficulty and add to chain
    def mine(self, block):
        # attempt to get the hash of the previous block.
        # this should raise an IndexError if this is the first block.
        try: block.previous_hash = self.chain[-1].hash()
        except IndexError: pass

        # loop until nonce that satisifeis difficulty is found
        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                # increase the nonce by one and try again
                block.nonce += 1

    # check if blockchain is valid
    def isValid(self, start_idx=1):
        # loop through blockchain
        for i in range(start_idx, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            # compare the previous hash to the actual hash of the previous block
            if _previous != _current or _current[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

if __name__ == '__main__':
    blockchain = Blockchain()
    database = ["hello", "goodbye", "test", "DATA here"]

    num = 0

    for data in database:
        num += 1
        blockchain.mine(Block(num, data=data))

    for block in blockchain.chain:
        print(block)

    print(blockchain.isValid())

    blockchain.chain[2].data = "NEW DATA"
    blockchain.mine(blockchain.chain[2])
    print(blockchain.isValid())
