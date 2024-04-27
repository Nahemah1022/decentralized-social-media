from hashlib import sha256
import struct

# Stringify and concatenate all arguments and produces a sha256 hash as a result
def hash(*args):
    hashing_text = ""; h = sha256()

    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

# The "block" of the blockchain. Points to the previous block by its unique hash in previous_hash.
class Block():
    def __init__(self, previous_hash="0"*64, data=None, nonce=0):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce

    # Compute a sha256 hash for the block's data.
    def hash(self):
        return hash(
            self.previous_hash,
            self.data,
            self.nonce
        )

    def encode(self):
        format_string = '32sI'  # 32-byte SHA256, 4-byte unsigned int
        header = struct.pack(format_string, self.previous_hash.encode('utf-8'), self.nonce)
        data = self.data
        if isinstance(data, str):
            data = data.encode('utf-8')
        return header + data
    
    @classmethod
    def decode(cls, block_data):
        format_string = '32sI'
        header_size = struct.calcsize(format_string)
        hs, nonce = struct.unpack(format_string, block_data[:header_size])
        return cls(hs, block_data[header_size:], nonce)

    # Returns a string of the block's data. Useful for diagnostic print statements.
    def __str__(self):
        return str("Block : Hash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
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
    def __init__(self, chain=[]):
        self.chain = chain

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
                return block
            else:
                # increase the nonce by one and try again
                block.nonce += 1

    # check if a block is valid to attach
    def isBlockValid(self, block):
        cur_hash = block.hash()
        return self.chain[-1].hash() == block.previous_hash and cur_hash[:self.difficulty] == "0" * self.difficulty

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
    database = [b"hello", b"goodbye", b"test", b"DATA here"]

    for data in database:
        mined_block = blockchain.mine(Block(data=data))
        blockchain.add(mined_block)

    for block in blockchain.chain:
        print(block)

    print(blockchain.isValid())

    # encoded_block = blockchain.chain[-1].encode()
    # print(encoded_block)
    # print(Block.decode(encoded_block))

    last_block = blockchain.chain[-1]
    blockchain.remove(blockchain.chain[-1])
    print(blockchain.isBlockValid(last_block))

    blockchain.chain[2].data = b"NEW DATA"
    blockchain.mine(blockchain.chain[2])
    print(blockchain.isValid())
