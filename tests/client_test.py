import pytest
import time
import random

from src import Tracker, P2PClient

def test_client_join():
    base_port = random.randint(49152, 65535)
    tracker = Tracker('localhost', base_port)
    num_of_clients = 4
    clients = []
    for i in range(num_of_clients):
        clients.append(P2PClient('localhost', base_port + 1 + i, 'localhost', base_port))
    time.sleep(3)
    for client in clients:
        assert len(client.peer_sockets) == num_of_clients - 1
    for client in clients:
        client.stop()
    tracker.stop()
