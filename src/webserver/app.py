from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import socket

from src.message import Message
from src.blockchain import Blockchain
from src.crypto import sign_data
from .socket_manager import SocketManager

app = Flask(__name__)

socket_manager = None

"""
curl -X GET http://localhost:5000/chain
"""
@app.route('/chain', methods=['GET'])
def get_chain():
    if not socket_manager.get_socket():
        return jsonify({"error": "No connection available"}), 400
    try:
        # Request the chain
        socket_manager.get_socket().sendall(Message('P', b'').pack())
        recv_msg = Message.recv_from(socket_manager.get_socket())
        blockchain = Blockchain.decode(recv_msg.payload)
        post_list = []
        for block in blockchain.chain:
            block_data = block.data.decode()
            post_list.append({
                "author": block_data[:64],
                "content": block_data[64:]
            })
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
    if not socket_manager.get_socket():
        return jsonify({"error": "No connection available"}), 400
    try:
        with open('public_key.pem', 'rb') as public_key_file:
            public_key_bytes = public_key_file.read()
        public_key_msg = Message('K', public_key_bytes).pack()
        signature = sign_data(post_content, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + post_content)
        socket_manager.get_socket().sendall(msg.pack())
        return jsonify({"status": "message sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_webserver(args):
    global socket_manager
    socket_manager = SocketManager((args.tracker_addr, args.tracker_port))
    socket_manager.update_connection()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=socket_manager.update_connection, trigger="interval", minutes=args.interval)
    scheduler.start()
    try:
        app.run(port=args.server_port, debug=True, use_reloader=False)  # Use reloader=False to not interfere with APScheduler
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

