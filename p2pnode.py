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
import json
from threading import Thread
import requests


class P2PNode:
    def __init__(self, tracker_host, tracker_port):
        self.peer_addrs = []
        self.tracker_addr = (tracker_host, tracker_port)
        self.peer_sockets = {}  # Stores TCP connections to peers

        self.tracker_socket = self.connect_to_tracker()
        self.self_addr = self.get_internal_ip()
        self.send_message_to_tracker(self.self_addr)

    def connect_to_tracker(self):
        """Establishes a TCP connection to the tracker."""
        try:
            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.connect(self.tracker_addr)
            print("[INFO] Connected to tracker.")
            Thread(target=self.listen_to_tracker,
                   args=(tracker_socket,)).start()
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

    def send_message_to_tracker(self, self_addr):
        add_node = {
            "action": "add_peer",
            "addr": self_addr,
        }
        message = json.dumps(add_node)
        self.tracker_socket.sendall(message.encode('utf-8'))

    def receive_messages(self, socket):
        """Receives messages from a socket."""
        try:
            while True:
                data = socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                print(f"[INFO] Received message: {message}")
        except Exception as e:
            print(f"[ERROR] Error receiving messages: {e}")
        finally:
            socket.close()

    def listen_to_tracker(self, tracker_socket):
        """Listens for messages from the tracker."""
        try:
            while True:
                data = tracker_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                print(f"[INFO] Received message from tracker: {message}")
                action = message.get('action')

                if action == 'add_peer':
                    self.peer_addrs = message.get('peers')
        except Exception as e:
            print(f"[ERROR] Error listening to tracker: {e}")
        finally:
            tracker_socket.close()

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
    node = P2PNode("localhost", 6789)
