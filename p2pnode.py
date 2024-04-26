# P2PNode
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
import websockets
import json

class P2PNode:
    def __init__(self, tracker_host, tracker_port):
        self.peer_addrs = []  # Will be filled with peer addresses as (host, port)
        self.tracker_addr = (tracker_host, tracker_port)  # Tracker address as (host, port)
        self.peer_websockets = {}  # Stores WebSocket connections to peers
        self.tracker_websocket = None  # WebSocket connection to the tracker

    async def connect_to_peer(self, peer_addr):
        try:
            websocket = await websockets.connect(f"ws://{peer_addr[0]}:{peer_addr[1]}")
            self.peer_websockets[peer_addr] = websocket
            # Consider starting a listener for each peer connection here
        except Exception as e:
            print(f"Failed to connect to peer {peer_addr}: {e}")

    async def disconnect_from_peer(self, peer_addr):
        websocket = self.peer_websockets.pop(peer_addr, None)
        if websocket:
            await websocket.close()

    async def connect_to_tracker(self):
        try:
            self.tracker_websocket = await websockets.connect(f"ws://{self.tracker_addr[0]}:{self.tracker_addr[1]}")
            # Send join event
            await self.peers_join()
        except Exception as e:
            print(f"Failed to connect to tracker: {e}")

    async def send_message(self, peer_addr, message):
        websocket = self.peer_websockets.get(peer_addr)
        if websocket:
            await websocket.send(json.dumps(message))

    async def peers_update(self, update_type, peer_addr):
        if update_type == 'join' and peer_addr not in self.peer_addrs:
            self.peer_addrs.append(peer_addr)
            await self.connect_to_peer(peer_addr)
        elif update_type == 'leave' and peer_addr in self.peer_addrs:
            self.peer_addrs.remove(peer_addr)
            await self.disconnect_from_peer(peer_addr)

    async def peers_leave(self):
        if self.tracker_websocket:
            await self.tracker_websocket.send(json.dumps({'event': 'leave'}))

    async def peers_join(self):
        if self.tracker_websocket:
            await self.tracker_websocket.send(json.dumps({'event': 'join'}))

    # Add a method to listen to the tracker
    async def listen_to_tracker(self):
        try:
            async for message in self.tracker_websocket:
                print(f"Received message from tracker: {message}")
        except Exception as e:
            print(f"Error listening to tracker: {e}")

async def main():
    node = P2PNode("localhost", 6789)
    await node.connect_to_tracker()
    await node.listen_to_tracker()

if __name__ == "__main__":
    asyncio.run(main())

