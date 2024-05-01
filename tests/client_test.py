import pytest
import time
import random

from src import Node, Tracker

def test_node_sockets():
    base_port = random.randint(49152, 65535)
    tracker = Tracker('localhost', base_port)
    num_of_nodes = 10
    nodes = []
    for i in range(num_of_nodes):
        nodes.append(Node(('localhost', base_port + i + 1), ('localhost', base_port)))
    time.sleep(num_of_nodes)
    for node in nodes:
        assert node._get_num_peers() == num_of_nodes - 1
    for node in nodes:
        node.stop()
    tracker.stop()
