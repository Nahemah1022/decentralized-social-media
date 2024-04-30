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
        if isinstance(data, str):
            data = data.encode('utf-8')

        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce

    # Compute a sha256 hash for the block's data.
    def hash(self):
        data = self.data
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hash(
            self.previous_hash,
            data,
            self.nonce
        )

    def encode(self):
        format_string = '64sII'  # 64-byte SHA256, 4-byte unsigned int, 4-byte unsigned int
        data = self.data
        if isinstance(data, str):
            data = data.encode('utf-8')
        header = struct.pack(format_string, self.previous_hash.encode('utf-8'), self.nonce, len(data))
        return header + data
    
    @classmethod
    def decode(cls, encoded_block):
        format_string = '64sII'
        header_size = struct.calcsize(format_string)
        prev_hs, nonce, _ = struct.unpack(format_string, encoded_block[:header_size])
        return cls(prev_hs.decode(), encoded_block[header_size:], nonce)

    # Returns a string of the block's data. Useful for diagnostic print statements.
    def __str__(self):
        data = self.data
        if isinstance(data, str):
            data = data.encode('utf-8')

        return str("Block : Hash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
            self.hash(),
            self.previous_hash,
            data,
            self.nonce
            )
        )


# A chain of the blocks.
class Blockchain():
    # the number of zeros in front of each hash
    difficulty = 4

    # restarts a new blockchain or the existing one upon initialization
    def __init__(self, chain=None):
        if chain is None:
            chain = []  # This creates a new list for each instance
        self.chain = chain
        self.block_table = {} # [(mined_block_hash, index_of_the_block_in_chain)]

    # add a new block to the chain
    def add(self, block):
        if self.isAttachableBlock(block):
            self.block_table[block.hash()] = len(self.chain)
            self.chain.append(block)

    # remove a block from the chain
    def remove(self, block):
        del self.block_table[block.hash()]
        self.chain.remove(block)

    # find the nonce of the block that satisfies the difficulty and add to chain
    def mine(self, block):
        # attempt to get the hash of the previous block.
        if len(self.chain) > 0:
            block.previous_hash = self.chain[-1].hash()
        # this should raise an IndexError if this is the first block.
        # try: block.previous_hash = self.chain[-1].hash()
        # except IndexError: pass

        # loop until nonce that satisifeis difficulty is found
        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                return block
            else:
                # increase the nonce by one and try again
                block.nonce += 1

    # check if a block is valid to attach
    def isAttachableBlock(self, block):
        if len(self.chain) == 0:
            return True
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
    
    # merge the remote chain into local chain by finding the fork point
    def mergeChain(self, remote_chain):
        for i, remote_block in enumerate(reversed(remote_chain)):
            # if the last block in the remote subchain exists in the local chain, 
            # it means local chain must be longer than remote chain => nothing to merge
            # therefore, we can just start from checking the second last block
            remote_subchain_len = i + 1
            if remote_block.previous_hash in self.block_table:
                fork_point = self.block_table[remote_block.previous_hash]
                # if length of forked remote subchain > forked local subchain, replace subchain
                if remote_subchain_len > len(self.chain) - fork_point - 1:
                    remote_idx = len(remote_chain) - remote_subchain_len
                    # Remove indice of replaced local subchain (keep fork point)
                    for j in range(fork_point + 1, len(self.chain)):
                        del self.block_table[self.chain[j].hash()]
                    self.chain = self.chain[:fork_point + 1]
                    self.chain.extend(remote_chain[remote_idx:])
                    # Add indice of merged remote subchain
                    for j in range(remote_idx, len(remote_chain)):
                        self.block_table[remote_chain[j].hash()] = (fork_point + 1) + (j - remote_idx)
                    return True
        return False
    
    def encode(self):
        res = b''
        for block in self.chain:
            res += block.encode()
        return res
    
    def print(self):
        for block in self.chain:
            print(block)
    
    @classmethod
    def decode(cls, encoded_blockchain):
        format_string = '64sII'
        header_size = struct.calcsize(format_string)
        bc = cls([])
        start = 0
        while start < len(encoded_blockchain):
            prev_hs, nonce, data_size = struct.unpack(format_string, encoded_blockchain[start:start + header_size])
            block = Block(prev_hs.decode(), encoded_blockchain[start + header_size:start + header_size + data_size], nonce)
            if not bc.isAttachableBlock(block):
                raise RuntimeError("The encoded blockchain is not valid")
            bc.add(block)
            start += header_size + data_size
        return bc

if __name__ == '__main__':
    # print("test basic mining function")
    # blockchain = Blockchain()
    # database = [b"hello", b"goodbye", b"test", b"DATA here"]
    # for data in database:
    #     mined_block = blockchain.mine(Block(data=data))
    #     blockchain.add(mined_block)
    # for block in blockchain.chain:
    #     print(block)
    # print(blockchain.isValid())

    # print("test isAttachableBlock() function")
    # last_block = blockchain.chain[-1]
    # blockchain.remove(blockchain.chain[-1])
    # print(blockchain.isAttachableBlock(last_block))

    # print("test Block's encode and decode functions")
    # print(Block.decode(last_block.encode()))

    # print("test immutability")
    # blockchain.chain[2].data = b"NEW DATA"
    # blockchain.mine(blockchain.chain[2])
    # print(blockchain.isValid())

    print("test merge function")
    base_database = [b"hello", b"goodbye"]
    bc1 = Blockchain()
    database1 = [b"test", b"DATA here"]
    for data in base_database:
        mined_block = bc1.mine(Block(data=data))
        bc1.add(mined_block)

    bc2 = Blockchain()
    bc2.chain = list(bc1.chain)
    bc2.block_table = bc1.block_table.copy()
    database2 = [b"changed", b"changed DATA here", b"I'm longer than the other chain"]

    for data in database1:
        mined_block = bc1.mine(Block(data=data))
        bc1.add(mined_block)

    # for block in bc1.chain:
    #     print(block)

    for data in database2:
        mined_block = bc2.mine(Block(data=data))
        bc2.add(mined_block)

    # for block in bc2.chain:
    #     print(block)

    bc1.mergeChain(bc2.chain)
    print(f"merged list is valid? {bc1.isValid()}")
    print("merged list: ")
    for block in bc1.chain:
        print(block)

    print("test Blockchain's encode and decode")
    decoded_bc = Blockchain.decode(bc1.encode())
    for block in decoded_bc.chain:
        print(block)
