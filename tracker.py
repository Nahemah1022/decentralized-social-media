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
import asyncio
import websockets
import json

class Tracker:
    def __init__(self):
        self.peers = {}  # Maps WebSocket connection to peer address
        self.users = {}  # Maps usernames to public keys

    async def register(self, username, public_key, websocket):
        if username in self.users:
            return False
        self.users[username] = public_key
        self.peers[websocket] = username
        return True

    async def get_user_public_key(self, username):
        """Retrieve the public key associated with the given username."""
        return self.users.get(username, None)  # Return None if username not found

    async def get_peers_addrs(self):
        """Return a list of addresses for all connected peers."""
        # remote_address: (host, port) like ('127.0.0.1', 6789)"
        return [str(ws.remote_address) for ws in self.peers if ws.open]

    async def broadcast(self, message):
        """Broadcast a message to all connected peers."""
        if self.peers:  # Ensure there are peers to broadcast to
            await asyncio.wait([peer.send(message) for peer in self.peers if peer.open])

    async def handle_connection(self, websocket, path):
        """Handle incoming WebSocket connections and messages."""
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    # Check if 'action' key is present in the received message
                    if 'action' not in data:
                        print("[WARNING] Received message without 'action' key.")
                        continue

                    if data['action'] == 'register':
                        success = await self.register(data['username'], data['public_key'], websocket)
                        await websocket.send(json.dumps({'action': 'register', 'success': success}))
                    elif data['action'] == 'get_peers':
                        peers = await self.get_peers_addrs()
                        await websocket.send(json.dumps({'action': 'get_peers', 'peers': peers}))
                    elif data['action'] == 'get_public_key':
                        public_key = await self.get_user_public_key(data['username'])
                        await websocket.send(json.dumps({'action': 'get_public_key', 'public_key': public_key}))
                except json.JSONDecodeError:
                    print("[ERROR] Invalid JSON received.")
                except KeyError as e:
                    print(f"[ERROR] Missing expected key in data: {e}")
        except Exception as e:
            print(f"[ERROR] Error handling connection: {e}")
        finally:
            # Cleanup when connection closes
            if websocket in self.peers:
                username = self.peers.pop(websocket, None)
                await self.broadcast(json.dumps({'action': 'peer_left', 'username': username}))
                print(f"[INFO] Connection closed for {path}")

async def main():
    tracker = Tracker()
    async with websockets.serve(tracker.handle_connection, "localhost", 6789):
        await asyncio.Future()  # Run until cancelled

if __name__ == "__main__":
    print("[DEBUG] Start tracker.py")
    asyncio.run(main())
    

