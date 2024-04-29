import socket
import select
import threading
import time

from blockchain import Block, Blockchain
from message import Message
from crypto import SIGNATURE_LEN, verify_signature, sign_data

class Node():
    def __init__(self, predefined_sockets=[]):
        self.bc = Blockchain()
        self.peer_sockets = predefined_sockets

        self.mempool = set()
        self.pool_lock = threading.Lock()
        self.pool_has_job_cond = threading.Condition(self.pool_lock)
        self.miner_thread = threading.Thread(target=self._mine_worker)
        self.miner_thread.start()
        self.event_thread = threading.Thread(target=self._recv_handler)
        self.event_thread.start()

    def _recv_handler(self):
        """
        _recv_handler() thread is dedicated to recieve incoming messages
        from the P2P network, and forward them to their corresponding handler function:
        1. [UPDATE PEER](addr) => __peer_update()
        2. [NEW BLOCK](signature, content) => __new_pending_block()
        3. [MINED BLOCK](block) => __mined_block()
        4. [PULL REQUEST](addr) => __push_local_chain()
        5. [RECIEVE CHAIN](addr) => merge remote chain
        """
        while True:
            ready_to_read, _, _ = select.select(self.peer_sockets, [], [], 1.0)
            for sock in ready_to_read:
                recv_msg = Message.recv_from(sock)
                print(recv_msg.type_char)
                if recv_msg.type_char == b'U':
                    self.__peer_update(recv_msg.payload)
                elif recv_msg.type_char == b'N':
                    signature = recv_msg.payload[:SIGNATURE_LEN]
                    block_data = recv_msg.payload[SIGNATURE_LEN:]
                    self.__new_pending_block(signature, block_data)
                elif recv_msg.type_char == b'M':
                    block = Block.decode(recv_msg.payload)
                    self.__mined_block(block, sock)
                elif recv_msg.type_char == b'P':
                    with self.pool_lock:
                        local_chain_msg = Message('R', self.bc.encode())
                    sock.sendall(local_chain_msg.pack())
                elif recv_msg.type_char == b'R':
                    remote_bc = Blockchain.decode(recv_msg.payload)
                    with self.pool_lock:
                        self.bc.mergeChain(remote_bc.chain)
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
    def __peer_update(self, data):
        print(data)

    # validate the signature, and push to mempool
    def __new_pending_block(self, signature, data):
        if not verify_signature(data, signature, 'public_key.pem'):
            print("invalid signature")
            return
        with self.pool_lock:
            self.mempool.add(data)
            self.pool_has_job_cond.notify(1)
            print(self.mempool)

    # validate the block, and add it to local blockchain
    def __mined_block(self, block, peer_sock):
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
            pull_msg = Message('R', b'')
            peer_sock.sendall(pull_msg.pack())

if __name__ == '__main__':
    sock1, sock2 = socket.socketpair()
    node = Node([sock2])

    database = [b"hello", b"goodbye", b"test", b"DATA here"]
    for data in database:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('N', signature + data)
        sock1.sendall(msg.pack())

    time.sleep(3)
    node.bc.print()
