from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import socket
import json

from src.message import Message
from src.blockchain import Blockchain
from src.crypto import sign_data

app = Flask(__name__)

current_node_addr = None
node_socket = None
tracker_addr = None

def update_connection():
    global current_node_addr, node_socket, tracker_addr
    try:
        if node_socket:
            node_socket.close()

        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.connect(tracker_addr)  # Tracker's address
        tracker_socket.sendall(Message('T', (1).to_bytes(4, 'big')).pack())
        recv_msg = Message.recv_from(tracker_socket)
        tracker_socket.close()

        if recv_msg.type_char == b'S':
            addr = socket.inet_ntoa(recv_msg.payload[:4])
            port_num = int.from_bytes(recv_msg.payload[4:6], 'big')
            current_node_addr = (addr, port_num)

            # Establish a new connection to the top node
            node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            node_socket.connect(current_node_addr)
    except Exception as e:
        print(f"Failed to update connection: {e}")

"""
curl -X GET http://localhost:5000/chain
"""
@app.route('/chain', methods=['GET'])
def get_chain():
    if not node_socket:
        return jsonify({"error": "No connection available"}), 400
    try:
        # Request the chain
        node_socket.sendall(Message('P', b'').pack())
        recv_msg = Message.recv_from(node_socket)
        blockchain = Blockchain.decode(recv_msg.payload)
        post_list = [block.data.decode() for block in blockchain.chain]
        return jsonify(post_list)  # Assuming Blockchain has a to_dict() method
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
curl -X POST http://localhost:5000/message \
-H "Content-Type: application/json" \
-d '{"post_content": "Mock Data"}'
"""
@app.route('/message', methods=['POST'])
def post_message():
    data = request.get_json()
    post_content = data["post_content"].encode('utf-8')
    print(post_content)
    if not node_socket:
        return jsonify({"error": "No connection available"}), 400
    try:
        with open('public_key.pem', 'rb') as public_key_file:
            public_key_bytes = public_key_file.read()
        public_key_msg = Message('K', public_key_bytes).pack()
        signature = sign_data(post_content, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + post_content)
        node_socket.sendall(msg.pack())
        return jsonify({"status": "message sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_webserver(args):
    global tracker_addr
    tracker_addr = (args.tracker_addr, args.tracker_port)
    update_connection()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_connection, trigger="interval", minutes=args.interval)
    scheduler.start()
    app.run(debug=True, use_reloader=False)  # Use reloader=False to not interfere with APScheduler
