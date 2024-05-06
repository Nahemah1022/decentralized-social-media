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
import threading
import requests
import time

from ..utils import AtomicBool
from ..message import Message

class P2PClient:
    def __init__(self, addr, tracker_addr, node_addr, join_handler, leave_handler, get_chain_len_cb, heartbeat_interval=5):
        self.heartbeat_interval = heartbeat_interval
        self.stop_event = threading.Event()
        self.running = AtomicBool(True)
        self.tracker_addr = tracker_addr
        if node_addr == None:
            node_addr = ('0.0.0.0', 0)
        self.node_addr = node_addr
        # self.peer_sockets = set()  # Stores TCP connections to peers

        self.join_handler = join_handler
        self.leave_handler = leave_handler
        self.get_chain_len_cb = get_chain_len_cb

        # 1st. create connector socket
        self.connector_socket = self.create_connector_socket(addr[0], addr[1])
        # 2nd. connect to tracker
        self.tracker_socket = self.connect_to_tracker()
        # 3rd. submit registration to tracker with the connector port
        self.event_thread = threading.Thread(target=self._event_handler)
        self.event_thread.start()
        self.tracker_socket.sendall(Message('R', addr[1].to_bytes(2, 'big') + socket.inet_aton(node_addr[0]) + node_addr[1].to_bytes(2, 'big')).pack())
        # 4th. heartbeat to tracker
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_handler)
        self.heartbeat_thread.start()

        # self.self_addr = self.get_internal_ip()

    def _event_handler(self):
        """Receives messages from a socket."""
        while self.running.get():
            ready_to_read, _, _ = select.select([self.tracker_socket, self.connector_socket], [], [], 0.1)
            for sock in ready_to_read:
                # At the beginning, recieve and connect to the list of peers from tracker
                if sock is self.tracker_socket:
                    try:
                        peer_list_msg = Message.recv_from(sock)
                        if peer_list_msg.type_char != b'L':
                            raise TypeError("Client recieve message other than type `L` from tracker")
                        for j in range(0, len(peer_list_msg.payload), 6):
                            peer_ip_addr = socket.inet_ntoa(peer_list_msg.payload[j:j+4])
                            peer_port = int.from_bytes(peer_list_msg.payload[j+4:j+6], 'big')
                            self.connect_to_peer((peer_ip_addr, peer_port))
                    except ConnectionAbortedError:
                        self._log("[ERROR] Disconnected from tracker. P2P client is down.")
                        return
                # Listen and accept incoming connections from other peers through connector socket
                elif sock is self.connector_socket:
                    peer_sock, addr = sock.accept()
                    self._log(f"[INFO] Incoming P2P connection from {addr}")
                    # self.peer_sockets.add(peer_sock)
                    self.join_handler(peer_sock)

    def _heartbeat_handler(self):
        while self.running.get():
            try:
                length = self.get_chain_len_cb()
                self.tracker_socket.sendall(Message('H', length.to_bytes(4, 'big')).pack())
                self.stop_event.wait(10)
            except KeyboardInterrupt:
                print("Stopped sending messages.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def create_connector_socket(self, host, port):
        connector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connector_socket.bind((host, port))
        connector_socket.listen(32)
        self._log(f"P2P client listening on {host}:{port}")
        return connector_socket

    def _log(self, *args):
        for arg in args:
            print(arg)

    def connect_to_tracker(self):
        """Establishes a TCP connection to the tracker."""
        try:
            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.connect(self.tracker_addr)
            self._log("[INFO] Connected to tracker.")
            return tracker_socket
        except Exception as e:
            print(f"[ERROR] Failed to connect to tracker: {e}")
            return None

    def connect_to_peer(self, peer_addr):
        """Establishes a TCP connection to a peer."""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_addr[0], peer_addr[1]))
            self._log(f"[INFO] Connected to peer at {peer_addr}.")
            self.join_handler(peer_socket)
            # self.peer_sockets.add(peer_socket)
        except Exception as e:
            print(f"[ERROR] Failed to connect to peer {peer_addr}: {e}")

    def stop(self):
        self.running.set(False)
        self.stop_event.set()
        # for peer_sock in self.peer_sockets:
        #     peer_sock.close()
        self.event_thread.join()
        self.heartbeat_thread.join()
        self.connector_socket.close()
        self.tracker_socket.close()

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
    node = P2PClient(("localhost", 8080), ("localhost", 6789))
