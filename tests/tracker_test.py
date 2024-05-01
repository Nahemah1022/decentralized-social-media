import pytest
import time
import socket

from src import Tracker

def test_tracker_join():
    tracker = Tracker('localhost', 6789)
    num_of_clients = 37
    client_sockets = []
    time.sleep(1)
    for i in range(num_of_clients):
        client_sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        client_sockets[i].connect(('localhost', 6789))
    
    time.sleep(3)

    assert len(tracker.clients_sockets) == num_of_clients
    tracker.stop()

if __name__ == '__main__':
    test_tracker_join()
