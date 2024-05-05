[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/-Lgd7v9y)
# CSEE 4119 Spring 2024, Class Project
## Team name: Fat Cat
## Team members (name, GitHub username):
- Yin-Tung Chen (yc4377), Nahemah1022
- Claire Chen (yc3387), yee-cee
- Junyao Duan (jd4024), rootofallevii
- Chia-Mei Liu (cl4424), madiliu 

## Getting Started

This project consists of multiple components that can be run independently. Below are the commands to start each service:

### Frontend

Before your first use, you would need to build the frontend.

```bash
cd frontend
npm install
npm run build
cd ..  # Go back to the root dir
```

### Tracker

To start the tracker service, use the following command. The tracker listens on a specified address and port.

```
python3 src/main.py tracker --tracker_addr='127.0.0.1' --tracker_port=8000
```

### Node

To start a node, run the following command. Nodes communicate with the tracker and other nodes, operating on specified P2P and node ports.

```
python3 src/main.py node --p2p_port=6000 --node_port=9000 --tracker_addr='127.0.0.1' --tracker_port=8000 --heartbeat_interval=10
```

### Webserver

To start the webserver that interfaces with the tracker and possibly nodes, use the command below:

```
python3 src/main.py webserver --server_port=5000 --tracker_addr='127.0.0.1' --tracker_port=8000 --interval=1
```

*Please replace this text with information on how to run your code, description of each file in the directory, and any assumptions you have made for your code*