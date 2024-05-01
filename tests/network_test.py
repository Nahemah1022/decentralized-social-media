import pytest
import time
import random

from src import Node, Tracker

def test_node_sockets():
    base_port = random.randint(49152, 65535)
    tracker = Tracker('localhost', base_port)
    num_of_nodes = 4
    nodes = []
    for i in range(num_of_nodes):
        nodes.append(Node(('localhost', base_port + i + 1), ('localhost', base_port)))
    time.sleep(3)
    for node in nodes:
        assert len(node.p2p_client.peer_sockets) == num_of_nodes - 1
    for node in nodes:
        node.stop()
    tracker.stop()
