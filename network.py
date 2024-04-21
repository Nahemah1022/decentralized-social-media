# network.py
import asyncio
import websockets

async def start_server(handler, host, port):
    async with websockets.serve(handler, host, port):
        await asyncio.Future()  # Run until cancelled

async def connect_to_server(uri):
    async with websockets.connect(uri) as websocket:
        return websocket  # The calling function will handle the websocket
