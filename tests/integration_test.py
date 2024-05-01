import pytest
import time
import random
import socket

from src import Node, Tracker, Message, sign_data

def test_two_nodes():
    app_send1, app_recv1 = socket.socketpair()
    app_send2, app_recv2 = socket.socketpair()

    base_port = random.randint(49152, 65535)
    tracker = Tracker('localhost', base_port)
    node1 = Node(
        p2p_addr=('localhost', base_port + 1), 
        tracker_addr=('localhost', base_port),
        app_sockets=[app_recv1])
    node2 = Node(p2p_addr=('localhost', base_port + 2), 
        tracker_addr=('localhost', base_port),
        app_sockets=[app_recv2])
    time.sleep(3)
    assert node1._get_num_peers() == 1
    assert node2._get_num_peers() == 1

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
    base_port = random.randint(49152, 65535)
    tracker = Tracker('localhost', base_port)
    num_nodes = 7
    app_socks = []
    nodes = []
    for i in range(num_nodes):
        app_socks.append(socket.socketpair())
        nodes.append(Node(
            p2p_addr=('localhost', base_port + 1 + i), 
            tracker_addr=('localhost', base_port),
            app_sockets=[app_socks[i][1]]))
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
        for app_send_sock, _ in app_socks:
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
        app_socks[random_node_idx][0].sendall(msg.pack())

    time.sleep(num_nodes)
    for node in nodes:
        assert node.bc.isValid()
        assert node._get_chain_len() == len(database) + len(chain_new)
        assert node.bc == nodes[0].bc

    for node in nodes:
        node.stop()
    tracker.stop()

if __name__ == '__main__':
    test_multi_nodes()
