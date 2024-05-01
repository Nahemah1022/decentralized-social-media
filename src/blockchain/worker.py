import socket
import select
import threading
import time

from .blockchain import Block, Blockchain, hash
from ..message import Message
from ..crypto import SIGNATURE_LEN, RSA_KEY_SIZE, verify_signature, sign_data
from ..utils import AtomicBool

class Worker():
    def __init__(self, predefined_sockets=None, enable_mining=True, name="default", log_filepath=None):
        self.log_lock = threading.Lock()
        self.log_file = None
        if log_filepath:
            self.log_file = open(f"{log_filepath}.log", 'w')
        self.running = AtomicBool(True)
        self.name = name
        self.bc = Blockchain()
        self.peer_socket_lock = threading.Lock()
        self.has_peer_cond = threading.Condition(self.peer_socket_lock)
        if predefined_sockets == None:
            predefined_sockets = []
        self.peer_sockets = set(predefined_sockets)

        self.mempool = set()
        self.pool_lock = threading.Lock()
        self.pool_has_job_cond = threading.Condition(self.pool_lock)

        self.enable_mining = AtomicBool(enable_mining)
        self.worker_thread = threading.Thread(target=self._mine_worker)
        self.worker_thread.start()
        self.event_thread = threading.Thread(target=self._recv_handler)
        self.event_thread.start()

    def _log(self, *args):
        return
        # if self.name != "node1":
        #     return
        with self.log_lock:
            if self.log_file:
                for arg in args:
                    print(f"{arg}", file=self.log_file)
            else:
                print(f"{self.name}:")
                for arg in args:
                    print(f"{arg}")

    def _recv_handler(self):
        """
        _recv_handler() thread is dedicated to recieve incoming messages
        from the P2P network, and forward them to their corresponding handler function:
        1. [UPDATE PEER](addr) => __peer_update()
        2. [NEW BLOCK](signature, content) => __new_pending_block(), from another peer
        3. [APP BLOCK](signature, content) => __new_pending_block(), from app
        4. [MINED BLOCK](block) => __mined_block()
        5. [PULL REQUEST](addr) => __push_local_chain()
        6. [CHAIN](addr) => merge remote chain
        """
        while True:
            with self.has_peer_cond:
                while len(self.peer_sockets) == 0:
                    self.has_peer_cond.wait()
                    if not self.running.get():
                        return
                ready_to_read, _, _ = select.select(list(self.peer_sockets), [], [], 0.1)
            # nothing to read and asked to stop => terminate
            if len(ready_to_read) == 0 and not self.running.get():
                return
            for sock in ready_to_read:
                # recv_msg = Message.recv_from(sock)
                try:
                    recv_msg = Message.recv_from(sock)
                    self._log(recv_msg.type_char)
                    if recv_msg.type_char == b'N':
                        public_key_msg, data = Message.unpack(recv_msg.payload)
                        public_key_bytes = public_key_msg.payload
                        signature = data[:SIGNATURE_LEN]
                        block_data = data[SIGNATURE_LEN:]
                        self._log(block_data)
                        self.__new_pending_block(signature, public_key_bytes, block_data)
                    elif recv_msg.type_char == b'A':
                        public_key_msg, data = Message.unpack(recv_msg.payload)
                        public_key_bytes = public_key_msg.payload
                        signature = data[:SIGNATURE_LEN]
                        block_data = data[SIGNATURE_LEN:]
                        self._log(block_data)
                        self.__new_pending_block(signature, public_key_bytes, block_data)

                        # forward the post from app to all peers
                        forward_msg = Message('N', recv_msg.payload)
                        for peer_sock in self.peer_sockets:
                            if peer_sock == sock:
                                continue
                            peer_sock.sendall(forward_msg.pack())
                    elif recv_msg.type_char == b'M':
                        block = Block.decode(recv_msg.payload)
                        self._log(block.data)
                        self.__mined_block(block, sock)
                    elif recv_msg.type_char == b'P':
                        with self.pool_lock:
                            local_chain_msg = Message('C', self.bc.encode())
                        sock.sendall(local_chain_msg.pack())
                    elif recv_msg.type_char == b'C':
                        remote_bc = Blockchain.decode(recv_msg.payload)
                        self._log(remote_bc)
                        with self.pool_lock:
                            fork_point, discarded_blocks = self.bc.mergeChain(remote_bc.chain)
                            # if blocks are acquired from remote, remove them from mempool to avoid to mine them again
                            for remote_idx in range(fork_point, len(self.bc.chain)):
                                remote_block = self.bc.chain[remote_idx]
                                if remote_block.data in self.mempool:
                                    self.mempool.remove(remote_block.data)
                            # re-mine discarded blocks
                            self._log(f"# hash pool: {self.bc.block_hash_pool}")
                            for block in discarded_blocks:
                                if hash(block.data) not in self.bc.block_hash_pool:
                                    self.mempool.add(block.data)
                        self._log("remote chain merged" if fork_point != -1 else "remote is shorter, reject to merge")
                        # print(f"isValid: {self.bc.isValid()}")
                    else:
                        raise TypeError("Invalid message type")
                    # with self.pool_lock:
                    #     self._log(self.bc)
                    #     self._log(self.mempool)
                    #     self._log("-------------")

                except ConnectionAbortedError:
                    self._peer_leave(sock)

    def _mine_worker(self):
        while True:
            with self.pool_has_job_cond:
                while len(self.mempool) == 0:
                    if not self.enable_mining.get():
                        return
                    self.pool_has_job_cond.wait()
                pending_block_data = next(iter(self.mempool))

            mined_block = self.bc.mine(Block(data=pending_block_data))
            self._log(f"# mined a block: {pending_block_data}")
            is_first = False
            with self.pool_lock:
                # otherwise, the block might have already been mined and propagates to this node
                if pending_block_data in self.mempool and self.bc.isAttachableBlock(mined_block):
                    is_first = True
                    self.mempool.remove(pending_block_data)
                    self.bc.add(mined_block)
            # if this node is the first one who successfully mined this block, broadcast it
            if is_first:
                mined_block_msg = Message('M', mined_block.encode())
                for peer_sock in self.peer_sockets:
                    peer_sock.sendall(mined_block_msg.pack())

    def stop(self):
        self.enable_mining.set(False)
        self.running.set(False)
        # invoke all conditional waiting threads
        with self.pool_has_job_cond:
            self.pool_has_job_cond.notify_all()
        with self.has_peer_cond:
            self.has_peer_cond.notify_all()
        self.worker_thread.join()
        # print(f"remaining pending blocks: {len(self.mempool)}")
        self.event_thread.join()
    
    def __del__(self):
        self.stop()

    def _get_num_peers(self):
        with self.peer_socket_lock:
            return len(self.peer_sockets)

    # add/remove the peer in local graph
    def _peer_join(self, sock):
        self._log(f"# peer connected at {sock}")
        with self.has_peer_cond:
            self.peer_sockets.add(sock)
            self.has_peer_cond.notify(1)

    def _peer_leave(self, sock):
        with self.peer_socket_lock:
            self.peer_sockets.remove(sock)

    # validate the signature, and push to mempool
    def __new_pending_block(self, signature, public_key_bytes, data):
        if not verify_signature(data, signature, public_key_bytes):
            print("invalid signature")
            return False
        with self.pool_lock:
            # discard any duplicated block
            if hash(data) in self.bc.block_hash_pool:
                return
            self.mempool.add(data)
            self.pool_has_job_cond.notify(1)

    # validate the block, and add it to local blockchain
    def __mined_block(self, block, peer_sock):
        if self.bc.isAttachableBlock(block):
            with self.pool_lock:
                # remove this valid block in mempool, and attach it to the current blockchain
                if block.data in self.mempool:
                    self.mempool.remove(block.data)
                self.bc.add(block)
        else:
            self._log("block unattachable")
            """
            If a node recieves a invalid block, there are three potential cases:
                1) fork happened
                2) missing blocks
                3) fake block
            For case 1) and 2) => The node will request the sender a subchain of blocks and identify 
                the fork point by comparing the local chain with each hash value in the subchain.
            For case 3) => must contains invalid block on the way back to root and will be detected.
            """
            pull_msg = Message('P', b'')
            peer_sock.sendall(pull_msg.pack())

if __name__ == '__main__':
    # print("test recieve mined block from peer")
    # sock1, sock2 = socket.socketpair()
    # sock3, sock4 = socket.socketpair()
    # node1 = Worker([sock1, sock3], enable_mining=False, name="node1")
    # node2 = Worker([sock2], enable_mining=True, name="node2")

    # database = [b"hello", b"goodbye", b"test", b"DATA here"]
    # for data in database:
    #     signature = sign_data(data, 'private_key.pem')
    #     msg = Message('A', signature + data)
    #     sock4.sendall(msg.pack())

    # time.sleep(3)
    # node1.bc.print()

    print("test merge longer blockchain")
    app_send1, app_recv1 = socket.socketpair()
    app_send2, app_recv2 = socket.socketpair()
    sock1, sock2 = socket.socketpair()
    node1 = Worker([app_recv1], enable_mining=True, name="node1")
    node2 = Worker([app_recv2], enable_mining=True, name="node2")

    # base blocks in both peers
    database = [b"hello", b"goodbye", b"test"]
    for data in database:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', signature + data)
        app_send1.sendall(msg.pack())
        app_send2.sendall(msg.pack())
    
    time.sleep(3)

    print("adding new blocks to peer1")
    # add some new blocks in peer1's chain
    chain1_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5"]
    for data in chain1_new:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', signature + data)
        app_send1.sendall(msg.pack())

    # wait for peer1 mining complete 
    time.sleep(3)

    # connect peer1 and peer2
    node1._peer_join(sock1)
    node2._peer_join(sock2)

    # send a new post to node2
    post = b"post block"
    signature = sign_data(post, 'private_key.pem')
    msg = Message('A', signature + post)
    app_send2.sendall(msg.pack())

    """
    both start mining this block of post at the same time
    peer2 will recieve the post directly, and peer1 will recieve it through peer2's forwarding
    case1: peer2 found a valid block and forward it to peer1:
      => unattachable, pull the whole chain
      => peer1's local chain is longer than peer2's remote chain
      => reject to merge
    case2: peer1 found a valid block and forward it to peer2:
      => unattachable, pull the whole chain
      => peer2's local chain is shorter than peer1's remote chain
      => merged and synchronized successfully
    """
    time.sleep(3)
    print("final result")
    node2.bc.print()
