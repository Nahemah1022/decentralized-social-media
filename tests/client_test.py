import pytest
import time
import random

from src import Node, Tracker, sign_data

def test_node_sockets():
    base_port = random.randint(49152, 65000)
    tracker = Tracker('127.0.0.1', base_port)
    num_of_nodes = 10
    nodes = []
    for i in range(num_of_nodes):
        nodes.append(Node(
            p2p_addr=('127.0.0.1', base_port + i + 1), 
            tracker_addr=('127.0.0.1', base_port),
            heartbeat_interval=1))
    time.sleep(num_of_nodes // 2)
    for node in nodes:
        assert node._get_num_peers() == num_of_nodes - 1
    for node in nodes:
        node.stop()
    tracker.stop()

def test_heartbeat_chain_length():
    base_port = random.randint(49152, 65000)
    tracker = Tracker('127.0.0.1', base_port)
    num_of_nodes = 7
    nodes = []
    node_ports = set()
    with open('public_key.pem', 'rb') as public_key_file:
        public_key_bytes = public_key_file.read()
    chain1_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5", b"chain1_6", b"chain1_7", b"chain1_8", b"chain1_9", b"chain1_10"]
    for i in range(num_of_nodes):
        node_ports.add(base_port + 2 * i + 2)
        nodes.append(Node(
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

    top_nodes = tracker._get_client_list(4)
    for n in top_nodes:
        port_num = int.from_bytes(n[0][4:], 'big')
        assert port_num in node_ports
        assert n[1] <= len(chain1_new)

    time.sleep(2)
    for node in nodes:
        node.stop()
    tracker.stop()

if __name__ == '__main__':
    test_heartbeat_chain_length()
