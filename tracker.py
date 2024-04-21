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
import json
from network import start_server

class Tracker:
    def __init__(self):
        self.active_nodes = set()

    async def handle_connection(self, websocket, path):
        # Register new node
        self.active_nodes.add(websocket)
        try:
            # Main event loop for the websocket
            async for message in websocket:
                # Here you would handle incoming messages such as node disconnects
                pass
        finally:
            # Unregister node
            self.active_nodes.remove(websocket)
            # Notify other nodes about the disconnect
            await self.broadcast(f"Node {path} disconnected")

    async def broadcast(self, message):
        # Broadcast a message to all connected nodes
        if self.active_nodes:  # Check if there are any connected nodes
            await asyncio.wait([node.send(message) for node in self.active_nodes])

async def main():
    tracker = Tracker()
    await start_server(tracker.handle_connection, "localhost", 6789)

if __name__ == "__main__":
    asyncio.run(main())
