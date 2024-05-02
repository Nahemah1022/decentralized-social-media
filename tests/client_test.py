import pytest
import time
import random

from src import Node, Tracker
import logging
logging.basicConfig(level=logging.DEBUG)

def test_node_sockets():
    base_port = random.randint(49152, 65000)
    tracker = Tracker('localhost', base_port)
    num_of_nodes = 10
    nodes = []
    for i in range(num_of_nodes):
        nodes.append(Node(
            p2p_addr=('localhost', base_port + i + 1), 
            tracker_addr=('localhost', base_port),
            heartbeat_interval=1))
    time.sleep(num_of_nodes // 2)
    for node in nodes:
        assert node._get_num_peers() == num_of_nodes - 1
    logging.debug("ternimating")
    for node in nodes:
        node.stop()
        logging.debug("stopped")
    tracker.stop()

def test_heartbeat_chain_length():
    base_port = random.randint(49152, 65000)
    tracker = Tracker('localhost', base_port)
    num_of_nodes = 4
    nodes = []
    for i in range(num_of_nodes):
        nodes.append(Node(
            p2p_addr=('localhost', base_port + i + 1), 
            tracker_addr=('localhost', base_port),
            heartbeat_interval=1))
    time.sleep(num_of_nodes // 2)
    for node in nodes:
        assert node._get_num_peers() == num_of_nodes - 1
    logging.debug("ternimating")
    for node in nodes:
        node.stop()
        logging.debug("stopped")
    tracker.stop()

if __name__ == '__main__':
    test_heartbeat_chain_length()
