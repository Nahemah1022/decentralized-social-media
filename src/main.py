import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.node import run_node
from src.p2p.tracker import run_tracker
from src.webserver import run_webserver

"""
python3 src/main.py tracker --tracker_addr='127.0.0.1' --tracker_port=8000
python3 src/main.py node --p2p_port=6000 --node_port=9000 --tracker_addr='127.0.0.1' --tracker_port=8000 --heartbeat_interval=1
python3 src/main.py webserver --server_port=5000 --tracker_addr='127.0.0.1' --tracker_port=8000 --interval=1
"""

def main():
    parser = argparse.ArgumentParser(description="Manage services for the project")
    subparsers = parser.add_subparsers(title="services", description="Available services", dest="service")
    subparsers.required = True

    # Node service
    parser_node = subparsers.add_parser('node', help='Start the node service')
    parser_node.add_argument('--p2p_port', type=int, required=True, help='Port for the p2p client to listen on')
    parser_node.add_argument('--node_port', type=int, required=True, help='Port for the node to listen on')
    parser_node.add_argument('--tracker_addr', type=str, required=True, help='IP address of p2p tracker')
    parser_node.add_argument('--tracker_port', type=int, required=True, help='Port of the p2p tracker')
    parser_node.add_argument('--heartbeat_interval', type=int, required=True, help='Interval in seconds for sending heartbeat to tracker')
    parser_node.set_defaults(func=run_node)

    # Tracker service
    parser_tracker = subparsers.add_parser('tracker', help='Start the tracker service')
    parser_tracker.add_argument('--tracker_addr', type=str, required=True, help='IP address for the tracker to listen on')
    parser_tracker.add_argument('--tracker_port', type=int, required=True, help='Port for the tracker to listen on')
    parser_tracker.set_defaults(func=run_tracker)

    # Webserver service
    parser_web = subparsers.add_parser('webserver', help='Start the webserver service')
    parser_web.add_argument('--server_port', type=str, required=True, help='Port for the webserver')
    parser_web.add_argument('--tracker_addr', type=str, required=True, help='IP address of p2p tracker')
    parser_web.add_argument('--tracker_port', type=int, required=True, help='Port of the p2p tracker')
    parser_web.add_argument('--interval', type=int, required=True, help='Interval in minutes for the webserver to update connected node')
    parser_web.set_defaults(func=run_webserver)

    args = parser.parse_args()
    args.func(args)  # Call the function associated with the chosen service

if __name__ == "__main__":
    main()
