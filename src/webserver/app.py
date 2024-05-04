from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import base64


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from src.message import Message
from src.blockchain import Blockchain
from src.crypto import sign_data, verify_signature
from .socket_manager import SocketManager

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True, support_credentials=True)

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

socket_manager = None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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
-d '{"post_content": "Mock Data", "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAurJefPtEOV45eWZr++3b\nsJ/HdKe2ZQ5hqP1/ww3qaMsxi+M8ADjwV8t9Xe8crMT33p48TiGbM6ygnCMc4bRu\n8QWwrSIuZe6E0Z2tW418ZgcyCoUQpmrod13/b4vWnYXzM92ZdM0UpYfDM0sGtmz/\nTb9ggmCEiIQ7tb3x/khTH7c/YdOaZys+3ELi05BSiNRGARBDKhoRCz2HhmkCPAOF\nvKtyF66oRh7uZTUE0XhG4zX495lCqY54ofL8Ak6uh/oK69OnUyIcqm2X79883ul3\ncRzVukqdtENzNGTJTIQLXMpiT4OOzu+PzM6uix6OwmXKkOt7mo2Vh+FNhM0Bee1h\nJQIDAQAB\n-----END PUBLIC KEY-----"}'
"""
@app.route('/message', methods=["POST", "OPTIONS"])
def post_message():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST": # The actual request following the preflight
        data = request.get_json()
        if "post_content" not in data:
            return _corsify_actual_response(jsonify({"error": "post_content field is required"})), 400
        post_content = data["post_content"].encode('utf-8')

        if not socket_manager.get_socket():
            return _corsify_actual_response(jsonify({"error": "No node connection available"})), 400
        try:
            if not "public_key" in data or not "signature" in data: # Sign by default keys pair
                print("Not both public_key and signature provided, sign the block by default keys pair")
                with open('public_key.pem', 'rb') as public_key_file:
                    public_key_data = public_key_file.read()
                signature = sign_data(post_content, 'private_key.pem')
            else:
                public_key_data = data["public_key"].encode()
                signature = base64.b64decode(data["signature"].encode())
                if not verify_signature(post_content, signature, public_key_data):
                    return _corsify_actual_response(jsonify({"status": "invalid signature"})), 400

            public_key_msg = Message('K', public_key_data).pack()

            msg = Message('A', public_key_msg + signature + post_content)
            socket_manager.get_socket().sendall(msg.pack())

            return _corsify_actual_response(jsonify({"status": "message sent"})), 200
        except Exception as e:
            print(e)
            return _corsify_actual_response(jsonify({"error": str(e)})), 500

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

