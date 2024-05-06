import pytest
import time
import random
import socket
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import Node
from src.p2p import Tracker
from src.crypto import sign_data
from src.message import Message

def test_node_sockets():
    base_port = random.randint(49152, 65000)
    tracker = Tracker('127.0.0.1', base_port, 'tracker')
    num_of_nodes = 10
    nodes = []
    for i in range(num_of_nodes):
        nodes.append(Node(
            log_filepath=f"node_{i}",
            p2p_addr=('127.0.0.1', base_port + i + 1), 
            tracker_addr=('127.0.0.1', base_port),
            heartbeat_interval=1))
    time.sleep(num_of_nodes)
    for node in nodes:
        assert node._get_num_peers() == num_of_nodes - 1
    for node in nodes:
        node.stop()
    tracker.stop()

def test_heartbeat_chain_length():
    base_port = random.randint(49152, 65000)
    tracker = Tracker('127.0.0.1', base_port, 'tracker')
    num_of_nodes = 7
    nodes = []
    node_ports = set()
    with open('public_key.pem', 'rb') as public_key_file:
        public_key_bytes = public_key_file.read()
    chain1_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5", b"chain1_6", b"chain1_7", b"chain1_8", b"chain1_9", b"chain1_10"]
    for i in range(num_of_nodes):
        node_ports.add(base_port + 2 * i + 2)
        nodes.append(Node(
            log_filepath=f"node_{i}",
            p2p_addr=('127.0.0.1', base_port + 2 * i + 1), 
            node_addr=('127.0.0.1', base_port + 2 * i + 2), 
            tracker_addr=('127.0.0.1', base_port),
            heartbeat_interval=1))
        # add some new blocks in peer1's chain
        database = chain1_new[:i]
        for data in database:
            signature = sign_data(data, 'private_key.pem')
            nodes[i]._new_pending_block(signature=signature, public_key_bytes=public_key_bytes, data=data)

    # time.sleep(2)
    # for node in nodes:
    #     assert node._get_num_peers() == num_of_nodes - 1

    top_k = 3
    # Retrieve from tracker
    top_nodes = tracker._get_client_list(top_k)
    for n in top_nodes:
        port_num = int.from_bytes(n[4:], 'big')
        assert port_num in node_ports
    
    # Retrieve from a new client socket
    mock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mock_socket.connect(('127.0.0.1', base_port))
    mock_socket.sendall(Message('T', top_k.to_bytes(4, 'big')).pack())
    recv_msg = Message.recv_from(mock_socket)
    assert recv_msg.type_char == b'S'
    for i in range(0, len(recv_msg.payload), 6): # 4 bytes of ip + 2 bytes of port number
        assert socket.inet_ntoa(recv_msg.payload[i:i+4]) == '127.0.0.1'
        port_num = int.from_bytes(recv_msg.payload[i+4:i+6], 'big')
        assert port_num in node_ports

    time.sleep(2)
    for node in nodes:
        node.stop()
    tracker.stop()

if __name__ == '__main__':
    test_heartbeat_chain_length()
