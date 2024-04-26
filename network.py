# network.py
import asyncio
import websockets

async def start_server(handler, host, port):
    server = await websockets.serve(handler, host, port)
    await server.wait_closed()  # This ensures the server runs indefinitely unless closed.

async def connect_to_server(uri):
    # Create a WebSocket connection that stays open for external use.
    websocket = await websockets.connect(uri)
    return websocket  # Let the caller handle the websocket lifecycle.
