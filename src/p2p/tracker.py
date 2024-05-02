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
        self.connected_sockets = {} # Map from connected but haven't registered clients to their address
        self.clients_sockets = {} # Map from peer's socket to peer's (address, port, chain_len)
        # self.clients_lock = threading.Lock()
        # self.has_client_cond = threading.Condition(self.clients_lock)
        self.server_socket = self.create_server_socket(host, port)
        self.event_thread = threading.Thread(target=self._event_handler)
        self.event_thread.start()

    def _log(self, *args):
        return
        for arg in args:
            print(arg)

    def _event_handler(self):
        """Handle each client connection in a separate thread."""
        while self.running.get():
            ready_to_read, _, _ = select.select(list(self.clients_sockets.keys()) + list(self.connected_sockets.keys()) + [self.server_socket], [], [], 0.1)
            for sock in ready_to_read:
                if sock is self.server_socket:
                    clnt_sock, addr = sock.accept() # step 1
                    # print(f"[INFO] Connection from {addr}")
                    self.connected_sockets[clnt_sock] = addr[0]
                else:
                    try:
                        recv_msg = Message.recv_from(sock)
                        # Client Registration for its previous connection
                        if recv_msg.type_char == b'R':
                            if len(recv_msg.payload) != 8:
                                raise ValueError("Registration message should has 2 bytes (size of the port number)")
                            
                            # form and respond with current peer list
                            current_peer_list = b''
                            for peer_addr, peer_port, _, _ in self.clients_sockets.values():
                                if peer_port == None: # Don't include non-registered clients
                                    continue
                                current_peer_list += socket.inet_aton(peer_addr)
                                current_peer_list += peer_port.to_bytes(2, 'big')
                            clnt_sock.sendall(Message('L', current_peer_list).pack()) # step 3

                            # register this socket to client list
                            port_num = int.from_bytes(recv_msg.payload[:2], 'big')
                            node_addr_bytes = recv_msg.payload[2:]
                            if sock in self.clients_sockets:
                                self._log("[WARNING] Multiple registration from registered client")
                                self.clients_sockets[sock] = (self.clients_sockets[sock][0], port_num, 0, node_addr_bytes)
                            elif sock in self.connected_sockets:
                                # move from not-registered pool to clients list
                                self.clients_sockets[sock] = (self.connected_sockets[sock], port_num, 0, node_addr_bytes)
                                del self.connected_sockets[sock]
                            else:
                                self._log("[ERROR] Registration from not connected client")
                        # Client periodical heartbeat
                        elif recv_msg.type_char == b'H':
                            clietn_chain_len = int.from_bytes(recv_msg.payload, 'big')
                            if sock in self.clients_sockets:
                                self.clients_sockets[sock] = (self.clients_sockets[sock][0], self.clients_sockets[sock][1], clietn_chain_len, self.clients_sockets[sock][3])
                            else:
                                self._log("[ERROR] Heartbeat from not registered client")                        
                    except ConnectionAbortedError:
                        if sock in self.clients_sockets:
                            del self.clients_sockets[sock]
                        if sock in self.connected_sockets:
                            del self.connected_sockets[sock]
                    except ConnectionResetError:
                        self._log("Connection was reset by the client.")

    def stop(self):
        self.running.set(False)
        self.event_thread.join()
        self.server_socket.close()
        for clnt_sock in self.clients_sockets:
            clnt_sock.close()

    def _get_client_list(self, top_k=None):
        if top_k == None:
            top_k = len(self.clients_sockets)
        top_k_list = sorted(self.clients_sockets.values(), key=lambda x: x[2], reverse=True)[:top_k]
        return [(node_addr, length) for _, _, length, node_addr in top_k_list]

    def create_server_socket(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(32)
        self._log(f"Tracker listening on {host}:{port}")
        return server_socket

if __name__ == "__main__":
    tracker = Tracker()
    HOST, PORT = 'localhost', 6789
