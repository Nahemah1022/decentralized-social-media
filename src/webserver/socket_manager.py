import socket
import threading

from src.message import Message

class SocketManager:
    def __init__(self, tracker_addr):
        self.node_socket = None
        self.tracker_addr = tracker_addr
        self.current_node_addr = None
        self.lock = threading.Lock()

    def get_socket(self):
        """Return the node_socket, reconnect if necessary."""
        with self.lock:
            if self.node_socket is None or self.is_socket_closed():
                print("Reconnecting due to closed socket or first-time connection.")
                self.update_connection()
            return self.node_socket

    def update_connection(self):
        """Connects to the tracker and updates node_socket based on tracker's response."""
        try:
            if self.node_socket:
                self.node_socket.close()
                self.node_socket = None

            tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tracker_socket.settimeout(5)  # Timeout for connecting to the tracker
            tracker_socket.connect(self.tracker_addr)
            tracker_socket.sendall(Message('T', (1).to_bytes(4, 'big')).pack())
            recv_msg = Message.recv_from(tracker_socket)
            tracker_socket.close()

            if recv_msg.type_char == b'S':
                addr = socket.inet_ntoa(recv_msg.payload[:4])
                port_num = int.from_bytes(recv_msg.payload[4:6], 'big')
                self.current_node_addr = (addr, port_num)
                print(f"[INFO] Trying to connect to node at {self.current_node_addr}")

                self.node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.node_socket.connect(self.current_node_addr)
                print(f"[INFO] Node connection changed to {self.current_node_addr}")
        except Exception as e:
            print(f"Failed to update connection: {e}")

    def is_socket_closed(self):
        """Check if the socket is closed by trying to read without blocking."""
        if not self.node_socket:
            return True
        try:
            self.node_socket.setblocking(0)
            data = self.node_socket.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # No data available
        except ConnectionResetError:
            return True  # Socket was closed by the other end
        finally:
            self.node_socket.setblocking(1)  # Reset socket to blocking mode
        return False

    def close_socket(self):
        """Close the current socket."""
        if self.node_socket:
            self.node_socket.close()
            self.node_socket = None
