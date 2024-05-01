import struct
import socket

HEADER_FORMAT = 'cQ'  # 'c' for character, 'Q' for 8-byte unsigned integer (Big Endian by default)

class Message:
    def __init__(self, type_char, payload):
        self.type_char = type_char.encode('utf-8')
        self.payload = payload
        self.size = len(payload)
    
    def pack(self):
        # Pack the type and size, followed by the payload
        header = struct.pack(HEADER_FORMAT, self.type_char, self.size)
        return header + self.payload

    @classmethod
    def unpack(cls, byte_data):
        header_size = struct.calcsize(HEADER_FORMAT)
        header = byte_data[:header_size]

        type_char, size = struct.unpack(HEADER_FORMAT, header)
        if len(byte_data) < header_size + size:
            raise ValueError("given byte_data's size is less than the size specified in header")
        payload = byte_data[header_size:header_size + size]
        rest = byte_data[header_size + size:]

        return cls(type_char.decode('utf-8'), payload), rest

    @classmethod
    def recv_from(cls, sock):
        header_size = struct.calcsize(HEADER_FORMAT)
        header = sock.recv(header_size)

        if len(header) == 0:
            raise ConnectionAbortedError("Connection closed by the other end of the socket")

        if len(header) < header_size:
            raise ValueError("Incomplete header received", len(header))

        type_char, payload_size = struct.unpack(HEADER_FORMAT, header)
        payload = bytearray()
        while len(payload) < payload_size:
            chunk = sock.recv(payload_size - len(payload))
            if not chunk:
                raise ValueError("Connection closed unexpectedly while reading payload")
            payload.extend(chunk)

        return cls(type_char.decode('utf-8'), bytes(payload))

if __name__ == '__main__':
    # Create a pair of connected sockets
    sock1, sock2 = socket.socketpair()

    # Create a test message and send it from sock1 to sock2
    message = Message('A', b'Hello, World!')
    packed_data = message.pack()
    sock1.sendall(packed_data)

    # Use recv_from to receive the message on sock2
    received_message = Message.recv_from(sock2)

    # Check if the received message matches the sent message
    assert received_message.type_char == b'A'
    assert received_message.size == len(b'Hello, World!')
    assert received_message.payload == b'Hello, World!'

    print("Test passed!")

    # Close the sockets
    sock1.close()
    sock2.close()
