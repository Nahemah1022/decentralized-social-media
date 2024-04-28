import socket
import select
import threading

from blockchain import Block, Blockchain, hash
from ..message import Message
from ..crypto import SIGNATURE_LEN, sign_data, verify_signature

class Node():
    def __init__(self):
        self.bc = Blockchain()
        self.peer_sockets = []

        self.mempool = set()
        self.pool_lock = threading.Lock()
        self.pool_has_job_cond = threading.Condition(self.pool_lock)
        self.miner_thread = threading.Thread(target=self._mine_worker)
        self.miner_thread.start()

    def _recv_handler(self):
        """
        _recv_handler() thread is dedicated to recieve incoming messages
        from the P2P network, and forward them to their corresponding handler function:
        1. [PEER](addr) => __peer_update()
        2. [NEW BLOCK](signature, content) => __new_pending_block()
        3. [MINED BLOCK](block) => __mined_block()
        4. [CHAIN PULL REQUEST](addr) => __push_local_chain()
        """
        while True:
            ready_to_read, _, _ = select.select(self.peer_sockets, [], [], 1.0)
            for sock in ready_to_read:
                peer_addr = sock.getpeername()[0]
                recv_msg = Message.recv_from(sock)
                print(recv_msg.type_char)
                if recv_msg.type_char == b'P':
                    self.__peer_update(recv_msg.payload, peer_addr)
                elif recv_msg.type_char == b'N':
                    signature = recv_msg.payload[:256]
                    block_data = recv_msg.payload[256:]
                    self.__new_pending_block(signature, block_data)
                elif recv_msg.type_char == b'M':
                    block = Block.decode(recv_msg.payload)
                    self.__mined_block(block, peer_addr)
                elif recv_msg.type_char == b'C':
                    # TODO: implement blockchain encode
                    sock.send(self.bc.encode())
                else:
                    raise TypeError("Invalid message type")

    def _mine_worker(self):
        while True:
            with self.pool_has_job_cond:
                while len(self.mempool) == 0:
                    self.pool_has_job_cond.wait()
                pending_block_data = next(iter(self.mempool))

            mined_block = self.bc.mine(Block(data=pending_block_data))
            with self.pool_lock:
                if pending_block_data in self.mempool:
                    self.mempool.remove(pending_block_data)
                    self.bc.add(mined_block)

    # add/remove the peer in local graph
    def __peer_update(self, data, peer_addr):
        print(data)

    # validate the signature, and push to mempool
    def __new_pending_block(self, signature, data):
        if not verify_signature(data, signature, 'public_key.pem'):
            return False
        with self.pool_lock:
            self.mempool.add(data)
            self.pool_has_job_cond.notify(1)

    # validate the block, and add it to local blockchain
    def __mined_block(self, block, peer_addr):
        if self.bc.isAttachableBlock(block):
            with self.pool_lock:
                # remove this valid block in mempool, and attach it to the current blockchain
                self.mempool.remove(block.data)
                self.bc.add(block)
        else:
            """
            If a node recieves a invalid block, there are three potential cases:
                1) fork happened
                2) missing blocks
                3) fake block
            For case 1) and 2) => The node will request the sender a subchain of blocks and identify 
                the fork point by comparing the local chain with each hash value in the subchain.
            For case 3) => must contains invalid block on the way back to root and will be detected.
            """
            subchain = self.pull_chain_from(peer_addr)
            self.bc.merge_chain(subchain)
