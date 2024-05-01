import pytest
import time
import socket

from src import Tracker, Message

def test_tracker_join():
    tracker = Tracker('localhost', 6789)
    num_of_clients = 40
    client_sockets = []
    base_port = 8000
    time.sleep(1)
    for i in range(num_of_clients):
        client_sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        client_sockets[i].connect(('localhost', 6789))
        port = base_port + i
        client_sockets[i].sendall(Message('R', port.to_bytes(2, 'big')).pack())
        peer_list_msg = Message.recv_from(client_sockets[i])
        assert peer_list_msg.type_char == b'L'
        assert len(peer_list_msg.payload) == i * 6 # 4 bytes ip address + 2 bytes port
        for j in range(0, len(peer_list_msg.payload), 6):
            ip_bytes = peer_list_msg.payload[j:j+4]
            port_bytes = peer_list_msg.payload[j+4:j+6]
            assert int.from_bytes(port_bytes, 'big') == base_port + j//6
            assert socket.inet_ntoa(ip_bytes) == '127.0.0.1'
    
    time.sleep(1)
    assert len(tracker.clients_sockets) == num_of_clients

    for i in range(num_of_clients // 2):
        client_sockets[i].close()

    time.sleep(1)
    assert len(tracker.clients_sockets) == num_of_clients // 2

    tracker.stop()

if __name__ == '__main__':
    test_tracker_join()
