# Decentralized Social Media

Decentralized Social Media (DSM) is a p2p system that maintains a blockchain of social media posts. Users are identified by public key, and authorized to his post using the signature signed by the corresponding private key. The blockchain holds the chain of contents of each individual post and the public key hash of its author.

## Getting Started

This project consists of multiple components that can be run independently. Below are the commands to start each service:

### Start by Docker Compose

Execute the following commands to spin up all service in one shot. You can modify the configuration for services in the `docker-compose.yml` file.

```
docker-compose build
docker-compose up -d
```

### Start Services Individually

To start the tracker service, use the following command. The tracker listens on a specified address and port.

```
python3 src/main.py tracker --tracker_addr='127.0.0.1' --tracker_port=8000
```

To start a node, run the following command. Nodes communicate with the tracker and other nodes, operating on specified P2P and node ports.

```
python3 src/main.py node --p2p_port=6000 --node_port=9000 --tracker_addr='127.0.0.1' --tracker_port=8000 --heartbeat_interval=10
```

To start the webserver that interfaces with the tracker and possibly nodes, use the command below:

```
python3 src/main.py webserver --server_port=5000 --tracker_addr='127.0.0.1' --tracker_port=8000 --interval=1
```

### Frontend

Before your first use, you would need to build the frontend.

```bash
cd frontend
npm install
npm run build
cd ..  # Go back to the root dir
```
