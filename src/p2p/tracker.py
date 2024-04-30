# Tracker
# Attributes:
# peers: Array - A list that keeps track of the active peer nodes in the network.
# users: Map - A dictionary that maps users' names to their public keys.

# Operations:
# broadcast(node, event): None - Broadcasts the given event to the entire P2P network. This could be a node joining or leaving the network.
# getPeersAddrs(): Array - Returns a list of addresses for all connected peers.
# register(username, public_key): Bool - Registers a new node with the given username and public key. Returns True on success, False if the username is already registered.
# getUserPublicKey(username): String - Retrieves the public key associated with the given username. Returns None if the username is not registered.

# Events:
# None specified, but typical events for a Tracker might include things like "onPeerJoin" and "onPeerLeave" to handle nodes connecting to and disconnecting from the network.

# tracker.py
import socket
import json
from threading import Thread


class Tracker:
    def __init__(self):
        self.clients = {}  # Maps client sockets to usernames
        self.users = {}  # Maps usernames to public keys

    def handle_connection(self, client_socket, addr):
        """Handle each client connection in a separate thread."""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                action = message.get('action')

                if action == 'register':
                    response = self.register(
                        message['username'], message['public_key'], client_socket)
                    client_socket.sendall(json.dumps(
                        {'action': 'register', 'success': response}).encode())
                elif action == 'get_peers':
                    peers = self.get_peers_addrs()
                    client_socket.sendall(json.dumps(
                        {'action': 'get_peers', 'peers': peers}).encode())
                elif action == 'get_public_key':
                    public_key = self.get_user_public_key(message['username'])
                    client_socket.sendall(json.dumps(
                        {'action': 'get_public_key', 'public_key': public_key}).encode())
                elif action == 'add_peer':
                    peers = self.get_peers_addrs().append(message.get('addr'))
                    client_socket.sendall(json.dumps(
                        {'action': 'add_peer', 'peers': peers}).encode())

        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON received.")
        except KeyError as e:
            print(f"[ERROR] Missing expected key in data: {e}")
        finally:
            self.disconnect_client(client_socket, addr)

    def register(self, username, public_key, client_socket):
        """Registers a new node with the given username and public key."""
        if username in self.users:
            return False
        self.users[username] = public_key
        self.clients[client_socket] = username
        return True

    def get_user_public_key(self, username):
        """Retrieves the public key associated with the given username."""
        return self.users.get(username, None)

    def get_peers_addrs(self):
        """Returns a list of addresses for all connected peers."""
        return [str(client.getpeername()) for client in self.clients if client]

    def broadcast(self, message):
        """Broadcasts a message to all connected peers."""
        for client in self.clients:
            try:
                client.sendall(json.dumps(message).encode())
            except:
                continue

    def disconnect_client(self, client_socket, addr):
        """Disconnects and removes a client."""
        client_socket.close()
        if client_socket in self.clients:
            del self.clients[client_socket]
        print(f"[INFO] Connection closed for {addr}")


def start_server(host, port, handler):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Tracker listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[INFO] Connection from {addr}")
        Thread(target=handler, args=(client_socket, addr)).start()


if __name__ == "__main__":
    tracker = Tracker()
    HOST, PORT = 'localhost', 6789
    start_server(HOST, PORT, tracker.handle_connection)
