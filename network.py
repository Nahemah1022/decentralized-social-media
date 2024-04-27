# network.py
import socket
from threading import Thread

def start_server(handler, host, port):
    """
    Starts a TCP server that listens on the specified host and port.
    For each incoming connection, it spawns a thread to handle that connection.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allows the socket to reuse the address
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        # Start a new thread to handle this specific client
        Thread(target=handler, args=(client_socket, addr)).start()

def connect_to_server(host, port):
    """
    Establishes a TCP connection to the specified host and port.
    Returns the socket object for further communication.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    return client_socket
