# P2PNode
# Attributes:
# peer_addrs: Array - A list of addresses (IP and port) for other peers this node can connect to.
# tracker_addr: Tuple - The address (IP and port) of the tracker node.

# Operations:
# None specified directly in the UML, but typical operations for a P2PNode would include:
# connect_to_peer(peer_addr): Establishes a connection to the peer at the given address.
# disconnect_from_peer(peer_addr): Closes the connection to the peer at the given address.
# connect_to_tracker(): Connects to the tracker to register itself and retrieve the list of peers.
# send_message(peer_addr, message): Sends a message to the peer at the given address.
# receive_message(): Handles incoming messages from peers.

# P2P Node
# connect_to_tracker()
# connect_to_peer()
#

# Tracker


# Events:
# InboundEvent
# peersUpdate(type, peer): Updates the local list of peers based on the given type of update (join or leave) and the peer's details.
# OutboundEvent
# peersLeave(self): Informs the tracker about this node's departure from the network.
# peersJoin(self): Informs the tracker about this node's arrival into the network.

# p2pnode.py
import socket
import select
from threading import Thread
import requests

from ..utils import AtomicBool
from ..message import Message

class P2PClient:
    def __init__(self, host, port, tracker_host, tracker_port):
        self.running = AtomicBool(True)
        self.tracker_addr = (tracker_host, tracker_port)
        self.peer_sockets = {}  # Stores TCP connections to peers

        self.tracker_socket = self.connect_to_tracker()
        self.self_addr = self.get_internal_ip()

        self.connector_socket = self.create_server_socket(host, port)

    def _event_handler(self):
        """Receives messages from a socket."""
        while self.running.get():
            ready_to_read, _, _ = select.select(list(self.clients_sockets.keys()) + [self.server_socket], [], [], 0.1)
            for sock in ready_to_read:
                if sock is self.tracker_socket:
                    peer_list_msg = Message.recv_from(sock)
                    for j in range(0, len(peer_list_msg.payload), 4):
                        ip_bytes = peer_list_msg.payload[j:j+4]
                        ip_addr = socket.inet_ntoa(ip_bytes)
                        # assert socket.inet_ntoa(ip_bytes) == '127.0.0.1'
                elif sock is self.connector_socket:
                    peer_sock, addr = sock.accept()

    def create_connector_socket(self, host, port):
        connector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connector_socket.bind((host, port))
        connector_socket.listen(32)
        self._log(f"Tracker listening on {host}:{port}")
        return connector_socket

    def connect_to_tracker(self):
        """Establishes a TCP connection to the tracker."""
        try:
            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.connect(self.tracker_addr)
            print("[INFO] Connected to tracker.")
            return tracker_socket
        except Exception as e:
            print(f"[ERROR] Failed to connect to tracker: {e}")
            return None

    def connect_to_peer(self, peer_addr):
        """Establishes a TCP connection to a peer."""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_addr[0], peer_addr[1]))
            self.peer_sockets[peer_addr] = peer_socket
            print(f"[INFO] Connected to peer at {peer_addr}.")
            Thread(target=self.receive_messages, args=(peer_socket,)).start()
        except Exception as e:
            print(f"[ERROR] Failed to connect to peer {peer_addr}: {e}")

    def disconnect_from_peer(self, peer_addr):
        """Closes the TCP connection to a peer."""
        peer_socket = self.peer_sockets.pop(peer_addr, None)
        if peer_socket:
            peer_socket.close()
            print(f"[INFO] Disconnected from peer at {peer_addr}.")

    def send_message(self, peer_addr, message):
        """Sends a message to a specified peer via TCP."""
        peer_socket = self.peer_sockets.get(peer_addr)
        if peer_socket:
            try:
                peer_socket.sendall(json.dumps(message).encode())
            except Exception as e:
                print(f"[ERROR] Failed to send message to {peer_addr}: {e}")

    def get_internal_ip():
        """
        Fetches the internal IP address of a Google Cloud VM instance using the metadata server.

        Returns:
            str: The internal IP address as a string, or None if an error occurs.

        Raises:
            Exception: Outputs an error message to the console if the metadata server cannot be reached.
        """
        metadata_url = 'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/ip'
        headers = {'Metadata-Flavor': 'Google'}
        try:
            response = requests.get(metadata_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text  # The internal IP address as a string
        except Exception as e:
            print(f"Error fetching internal IP from metadata server: {e}")
            return None


if __name__ == "__main__":
    node = P2PClient("localhost", 8080, "localhost", 6789)
