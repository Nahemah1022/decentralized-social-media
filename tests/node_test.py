import pytest
import time
import random
import socket
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import Node
from src.p2p import Tracker
from src.message import Message
from src.blockchain import Blockchain
from src.crypto import sign_data

def test_two_nodes():
    app_send1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_send2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    base_port = random.randint(49152, 65535)
    tracker = Tracker('127.0.0.1', base_port, 'tracker')
    node1 = Node(
        log_filepath="node_1",
        p2p_addr=('127.0.0.1', base_port + 1), 
        node_addr=('127.0.0.1', base_port + 3), 
        tracker_addr=('127.0.0.1', base_port))
    node2 = Node(
        log_filepath="node_2",
        p2p_addr=('127.0.0.1', base_port + 2), 
        node_addr=('127.0.0.1', base_port + 4), 
        tracker_addr=('127.0.0.1', base_port))
    
    time.sleep(3)
    assert node1._get_num_peers() == 1
    assert node2._get_num_peers() == 1
    
    app_send1.connect(('127.0.0.1', base_port + 3))
    app_send2.connect(('127.0.0.1', base_port + 4))

    # base blocks in both peers
    database = [b"hello", b"goodbye", b"test"]
    with open('public_key.pem', 'rb') as public_key_file:
        public_key_bytes = public_key_file.read()
    public_key_msg = Message('K', public_key_bytes).pack()
    for data in database:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + data)
        app_send1.sendall(msg.pack())
        app_send2.sendall(msg.pack())

    # time.sleep(3)
    # assert node1.bc.isValid()
    # assert node2.bc.isValid()
    # assert len(node1.bc.chain) == len(database)
    # assert len(node2.bc.chain) == len(database)

    # add some new blocks in peer1's chain
    chain1_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5"]
    for data in chain1_new:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + data)
        app_send1.sendall(msg.pack())

    # send a new post to node2
    post = b"post block"
    signature = sign_data(post, 'private_key.pem')
    msg = Message('A', public_key_msg + signature + post)
    app_send2.sendall(msg.pack())

    time.sleep(3)
    assert node1.bc.isValid()
    assert node2.bc.isValid()
    assert len(node1.bc.chain) == len(database) + len(chain1_new) + 1
    assert len(node2.bc.chain) == len(database) + len(chain1_new) + 1

    node1.stop()
    node2.stop()
    tracker.stop()

def test_multi_nodes():
    base_port = random.randint(49152, 65000)
    tracker = Tracker('127.0.0.1', base_port, 'tracker')
    num_nodes = 7
    app_socks = []
    nodes = []
    for i in range(num_nodes):
        app_socks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        nodes.append(Node(
            log_filepath=f"node_{i}",
            p2p_addr=('127.0.0.1', base_port + 1 + i * 2), 
            node_addr=('127.0.0.1', base_port + 2 + i * 2), 
            tracker_addr=('127.0.0.1', base_port)))
        app_socks[i].connect(('127.0.0.1', base_port + 2 + i * 2))
        time.sleep(i)
        assert nodes[i]._get_num_peers() == i

    # base blocks in both peers
    database = [b"hello", b"goodbye", b"test"]
    with open('public_key.pem', 'rb') as public_key_file:
        public_key_bytes = public_key_file.read()
    public_key_msg = Message('K', public_key_bytes).pack()
    for data in database:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + data)
        for app_send_sock in app_socks:
            app_send_sock.sendall(msg.pack())

    # time.sleep(3)
    # for node in nodes:
    #     assert node._get_chain_len() == len(database)

    # add new blocks to randomly-chosen node
    chain_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5"]
    for data in chain_new:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + data)
        random_node_idx = random.randint(0, num_nodes - 1)
        app_socks[random_node_idx].sendall(msg.pack())

    time.sleep(num_nodes * 2)
    for node in nodes:
        assert node.bc.isValid()
        assert node._get_chain_len() == len(database) + len(chain_new)
        assert node.bc == nodes[0].bc

    for node in nodes:
        node.stop()
    tracker.stop()

def test_pull_chain_from_longest_node():
    base_port = random.randint(49152, 65000)
    tracker_addr = ('127.0.0.1', base_port)
    tracker = Tracker('127.0.0.1', base_port, 'tracker')
    num_nodes = 4
    app_socks = []
    nodes = []
    for i in range(num_nodes):
        app_socks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        nodes.append(Node(
            log_filepath=f"node_{i}",
            p2p_addr=('127.0.0.1', base_port + 1 + i * 2), 
            node_addr=('127.0.0.1', base_port + 2 + i * 2), 
            tracker_addr=('127.0.0.1', base_port)))
        app_socks[i].connect(('127.0.0.1', base_port + 2 + i * 2))

    # base blocks in both peers
    database = [b"hello", b"goodbye", b"test"]
    with open('public_key.pem', 'rb') as public_key_file:
        public_key_bytes = public_key_file.read()
    public_key_msg = Message('K', public_key_bytes).pack()
    for data in database:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + data)
        for app_send_sock in app_socks:
            app_send_sock.sendall(msg.pack())

    # time.sleep(3)
    # for node in nodes:
    #     assert node._get_chain_len() == len(database)

    # add new blocks to randomly-chosen node
    chain_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5"]
    for data in chain_new:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + data)
        random_node_idx = random.randint(0, num_nodes - 1)
        app_socks[random_node_idx].sendall(msg.pack())

    # time.sleep(num_nodes)
    # for node in nodes:
    #     assert node.bc.isValid()
    #     assert node._get_chain_len() == len(database) + len(chain_new)
    #     assert node.bc == nodes[0].bc

    time.sleep(3)

    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.connect(tracker_addr)
    top_k = 3
    tracker_socket.sendall(Message('T', top_k.to_bytes(4, 'big')).pack())
    recv_msg = Message.recv_from(tracker_socket)
    assert recv_msg.type_char == b'S'
    addr = socket.inet_ntoa(recv_msg.payload[:4])
    port_num = int.from_bytes(recv_msg.payload[4:6], 'big')
    node_addr = (addr, port_num)

    print(node_addr)

    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.connect(node_addr)
    node_socket.sendall(Message('P', b'').pack())
    recv_msg = Message.recv_from(node_socket)
    assert recv_msg.type_char == b'C'
    remote_bc = Blockchain.decode(recv_msg.payload)
    assert len(remote_bc.chain) <= len(database) + len(chain_new)
    assert remote_bc.isValid()

    for node in nodes:
        node.stop()
    tracker.stop()

if __name__ == '__main__':
    test_pull_chain_from_longest_node()
