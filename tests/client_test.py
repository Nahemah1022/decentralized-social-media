import pytest
import time

from src import Tracker, P2PClient

def test_client_join():
    tracker = Tracker('localhost', 6789)
    num_of_clients = 4
    base_port = 8000
    clients = []
    for i in range(num_of_clients):
        clients.append(P2PClient('localhost', base_port + i, 'localhost', 6789))
    time.sleep(3)
    for client in clients:
        assert len(client.peer_sockets) == num_of_clients - 1
    for client in clients:
        client.stop()
    tracker.stop()
