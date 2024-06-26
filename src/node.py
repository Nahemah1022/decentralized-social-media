import socket
import select
import threading
import time

from .blockchain import Worker
from .p2p import P2PClient
from .message import Message
from .crypto import SIGNATURE_LEN

class Node(Worker):
    def __init__(self, p2p_addr, tracker_addr, node_addr=None, app_sockets=None, enable_mining=True, name="default", log_filepath=None, heartbeat_interval=5):
        super().__init__(enable_mining, name, log_filepath)
        self.p2p_client = P2PClient(p2p_addr, tracker_addr, node_addr, self._peer_join, self._peer_leave, self._get_chain_len, heartbeat_interval)
        if app_sockets == None:
            app_sockets = []
        self.app_sockets = set(app_sockets)
        self.app_sockets_lock = threading.Lock()

        self.node_addr = node_addr
        if self.node_addr: # expose the node server to web-server
            self.server_socket = self.create_server(node_addr)
            self._app_recv_thread = threading.Thread(target=self._app_recv_handler)
            self._app_recv_thread.start()

    def _app_recv_handler(self):
        while True:
            with self.app_sockets_lock:
                ready_to_read, _, _ = select.select(list(self.app_sockets) + [self.server_socket], [], [], 0.1)
            # nothing to read and asked to stop => terminate
            if len(ready_to_read) == 0 and not self.running.get():
                return
            for sock in ready_to_read:
                if sock is self.server_socket:
                    app_sock, addr = self.server_socket.accept()
                    self._log(f"[Node] Accept new app connection from {addr}")
                    with self.app_sockets_lock:
                        self.app_sockets.add(app_sock)
                else:
                    try:
                        recv_msg = Message.recv_from(sock)
                        self._log(f"[Node] Recieved message with type {recv_msg.type_char}")
                        if recv_msg.type_char == b'A':
                            public_key_msg, data = Message.unpack(recv_msg.payload)
                            public_key_bytes = public_key_msg.payload
                            signature = data[:SIGNATURE_LEN]
                            block_data = data[SIGNATURE_LEN:]
                            self._log(block_data)
                            self._new_pending_block(signature, public_key_bytes, block_data)

                            # forward the post from app to all peers
                            forward_msg = Message('N', recv_msg.payload)
                            with self.peer_socket_lock:
                                for peer_sock in self.peer_sockets:
                                    peer_sock.sendall(forward_msg.pack())
                        elif recv_msg.type_char == b'P':
                            with self.pool_lock:
                                local_chain_msg = Message('C', self.bc.encode())
                            sock.sendall(local_chain_msg.pack())
                    except ConnectionAbortedError:
                        with self.app_sockets_lock:
                            self.app_sockets.remove(sock)

    def create_server(self, node_addr):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(node_addr)
        server_socket.listen(32)
        self._log(f"[Node] app server listening on {node_addr[0]}:{node_addr[1]}")
        return server_socket

    def __del__(self):
        self.stop()
        return super().__del__()

    def stop(self):
        super().stop()
        self.p2p_client.stop()
        if self.node_addr:
            self._app_recv_thread.join()

def run_node(args):
    node = Node(
        p2p_addr=('0.0.0.0', args.p2p_port), 
        node_addr=('0.0.0.0', args.node_port), 
        tracker_addr=(args.tracker_addr, args.tracker_port),
        heartbeat_interval=args.heartbeat_interval
    )
    try:
        print("Node started. Press Ctrl+C to stop.")
        while True:
            time.sleep(10)  # Sleep for a long time, effectively waiting indefinitely
    except KeyboardInterrupt:
        print("Node interrupted by user.")
    node.stop()
