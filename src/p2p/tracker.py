# Tracker
# Attributes:
# peers: Array - A list that keeps track of the active peer nodes in the network.
# users: Map - A dictionary that maps users' names to their public keys.

# Operations:
# broadcast(node, event): None - Broadcasts the given event to the entire P2P network. This could be a node joining or leaving the network.
# getPeersAddrs(): Array - Returns a list of addresses for all connected peers.
# register(username, public_key): Bool - Registers a new node with the given username and public key. Returns True on success, False if the username is already registered.
# getUserPublicKey(username): String - Retrieves the public key associated with the given username. Returns None if the username is not registered.

# Events:
# None specified, but typical events for a Tracker might include things like "onPeerJoin" and "onPeerLeave" to handle nodes connecting to and disconnecting from the network.

# tracker.py
import socket
import select
import threading

from ..message import Message
from ..utils import AtomicBool

class Tracker:
    def __init__(self, host, port):
        self.running = AtomicBool(True)
        self.clients_sockets = {} # Map from peer's socket to peer's address
        # self.clients_lock = threading.Lock()
        # self.has_client_cond = threading.Condition(self.clients_lock)
        self.server_socket = self.create_server_socket(host, port)
        self.event_thread = threading.Thread(target=self._event_handler)
        self.event_thread.start()

    def _log(self, *args):
        for arg in args:
            print(arg)

    def _event_handler(self):
        """Handle each client connection in a separate thread."""
        while self.running.get():
            ready_to_read, _, _ = select.select(list(self.clients_sockets.keys()) + [self.server_socket], [], [], 0.1)
            for sock in ready_to_read:
                if sock is self.server_socket:
                    clnt_sock, addr = sock.accept() # step 1
                    # print(f"[INFO] Connection from {addr}")

                    current_peer_list = b''
                    for peer_addr in self.clients_sockets.values():
                        current_peer_list += socket.inet_aton(peer_addr)
                    self.clients_sockets[clnt_sock] = addr[0] # step 2

                    clnt_sock.sendall(Message('L', current_peer_list).pack()) # step 3
                else:
                    recv_msg = sock.recv(1024)
                    if recv_msg == b'':
                        del self.clients_sockets[sock]
                    else:
                        raise ValueError(f"Tracker is not supposed to recieve any message except zero-byte, but got {recv_msg}")

    def stop(self):
        self.running.set(False)
        self.event_thread.join()

    def create_server_socket(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(32)
        print(f"Tracker listening on {host}:{port}")
        return server_socket

if __name__ == "__main__":
    tracker = Tracker()
    HOST, PORT = 'localhost', 6789
