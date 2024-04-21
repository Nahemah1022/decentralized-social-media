# Attributes:
# peer_addrs: Array - A list of addresses (IP and port) for other peers this node can connect to.
# tracker_addr: Tuple - The address (IP and port) of the tracker node.

# Operations:
# None specified directly in the UML, but typical operations for a P2PNode would include:
# connect_to_peer(peer_addr): Establishes a connection to the peer at the given address.
# disconnect_from_peer(peer_addr): Closes the connection to the peer at the given address.
# connect_to_tracker(): Connects to the tracker to register itself and retrieve the list of peers.
# send_message(peer_addr, message): Sends a message to the peer at the given address.
# receive_message(): Handles incoming messages from peers.

# Events:
# InboundEvent
# peersUpdate(type, peer): Updates the local list of peers based on the given type of update (join or leave) and the peer's details.
# OutboundEvent
# peersLeave(self): Informs the tracker about this node's departure from the network.
# peersJoin(self): Informs the tracker about this node's arrival into the network.

# p2pnode.py
import asyncio
import json
from network import connect_to_server

class P2PNode:
    def __init__(self, tracker_uri):
        self.tracker_uri = tracker_uri
        self.peer_sockets = set()

    async def connect_to_tracker(self):
        self.tracker_socket = await connect_to_server(self.tracker_uri)
        # Send a message to the tracker to register or request peer list, etc.

    async def listen_to_tracker(self):
        # This method handles incoming messages from the tracker
        async for message in self.tracker_socket:
            # Process message from the tracker
            print(f"Received message from tracker: {message}")

    async def connect_to_peer(self, peer_uri):
        # This method would handle peer connections
        peer_socket = await connect_to_server(peer_uri)
        self.peer_sockets.add(peer_socket)
        # Listen to messages from peers, etc.

async def main():
    node = P2PNode("ws://localhost:6789")
    await node.connect_to_tracker()
    await node.listen_to_tracker()

if __name__ == "__main__":
    asyncio.run(main())
