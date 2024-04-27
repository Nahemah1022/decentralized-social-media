import socket
import select

from blockchain import Block, Blockchain
from ..message import Message

class Node():
    def __init__(self):
        self.bc = Blockchain()
        self.mempool = []
        self.peer_sockets = {} # [(addr1, socket1), (addr2, socket2), ...]
        self.msg_header_size = Message.get_header_size()

    def _recv_handler(self):
        """
        _recv_handler() thread is dedicated to recieve incoming messages
        from the P2P network, and forward them to their corresponding handler function:
        1. [PEER](addr) => __peer_update()
        2. [NEW BLOCK](signature, content) => __new_pending_block()
        3. [MINED BLOCK](block) => __mined_block()
        """
        while True:
            ready_to_read, _, _ = select.select(self.peer_sockets.values(), [], [], 1.0)
            for sock in ready_to_read:
                received_message = Message.recv_from(sock)
                print(received_message.type_char)
                print(received_message.size)
                print(received_message.payload)

    # add/remove the peer in local graph
    def __peer_update(self):
        pass

    # validate the signature, and push to mempool
    def __new_pending_block(self):
        pass

    # validate the block, and add it to local blockchain
    def __mined_block(self):
        """
        If a node recieves a invalid block, there are two potential cases:
            1) a fork happened
            2) missing blocks
            3) fake block
        For case 1) and 2) => The node will request the sender a subchain of blocks and identify 
            the fork point by comparing the local chain with each hash value in the subchain.
        For case 3) => must contains invalid block on the way back to root and will be detected.
        """
        pass
