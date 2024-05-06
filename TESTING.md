# Testing for Decentralized Social Media Application

## Introduction
This file describes the testing strategy and implementation details for the Decentralized Social Media Application. The system combines blockchain technology with a peer-to-peer (P2P) networking model to offer a robust platform for social media interactions. Key components include Node operations, Tracker functionalities, and block mining processes, all of which are critical to the system's performance and reliability.

## Test Environment Setup
Before executing the tests, ensure that the system is configured correctly:
1. Python version: Python 3.8 or higher.
2. Required libraries: pytest, pyOpenSSL, socket, os, time, and random.
eg:
    ```
    python3 -m pip install pytest
    ```
3. Set up virtual environment and install dependencies using:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Running the Tests
For each of the 4 test files in tests/, use:
```
python3 -m pytest path/to/test_file.py
```
eg:
```
python3 -m pytest tests/node_test.py
```

## Test Files Description
Tests are organized across several scripts to validate different components of the system:

### 1. `client_test.py`
Tests the functionality and stability of client nodes within the P2P network.
- **test_node_sockets**: Validates that all nodes can successfully create and manage their network sockets.
- **test_heartbeat_chain_length**: Ensures that heartbeats correctly reflect the blockchain's length and that the tracker can aggregate and provide accurate network data.

### 2. `node_test.py`
Similar to `client_test.py`, focuses on node interactions and network dynamics.
- **test_node_sockets**: Confirms proper socket operation and peer discovery.
- **test_heartbeat_chain_length**: Tests the ability of nodes to maintain accurate and consistent views of the blockchain across different network states.

### 3. `tracker_test.py`
Validates the tracker's ability to manage node lists and handle node connectivity.
- **test_tracker_join**: Ensures the tracker can handle node registrations and maintain an accurate list of active nodes.

### 4. `worker_test.py`
Focuses on the blockchain worker's ability to handle mining and chain synchronization.
- **test_merge_longer_chain**: Checks that the blockchain synchronization logic correctly merges chains of differing lengths based on the longest valid chain principle.

## Test Results
### 1. `client_test.py`
```
python3 -m pytest tests/client_test.py
```
```
====================== test session starts =======================
platform linux -- Python 3.8.10, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/yc3387/project-fat-cat
collected 2 items                                                

tests/client_test.py F.                                    [100%]

============================ FAILURES ============================
_______________________ test_node_sockets ________________________

    def test_node_sockets():
        base_port = random.randint(49152, 65000)
        tracker = Tracker('127.0.0.1', base_port, 'tracker')
        num_of_nodes = 10
        nodes = []
        for i in range(num_of_nodes):
            nodes.append(Node(
                log_filepath=f"node_{i}",
                p2p_addr=('127.0.0.1', base_port + i + 1),
                tracker_addr=('127.0.0.1', base_port),
                heartbeat_interval=1))
        time.sleep(num_of_nodes)
        for node in nodes:
>           assert node._get_num_peers() == num_of_nodes - 1
E           assert 7 == (10 - 1)
E            +  where 7 = <bound method Worker._get_num_peers of <src.node.Node object at 0x7f600d0ec1c0>>()
E            +    where <bound method Worker._get_num_peers of <src.node.Node object at 0x7f600d0ec1c0>> = <src.node.Node object at 0x7f600d0ec1c0>._get_num_peers

tests/client_test.py:28: AssertionError
---------------------- Captured stdout call ----------------------
P2P client listening on 127.0.0.1:54507
[INFO] Connected to tracker.
P2P client listening on 127.0.0.1:54508
[INFO] Connected to tracker.
[INFO] Incoming P2P connection from ('127.0.0.1', 35208)
[INFO] Connected to peer at ('127.0.0.1', 54507).
P2P client listening on 127.0.0.1:54509
[INFO] Connected to tracker.
[INFO] Incoming P2P connection from ('127.0.0.1', 35210)
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Incoming P2P connection from ('127.0.0.1', 32982)
[INFO] Connected to peer at ('127.0.0.1', 54508).
P2P client listening on 127.0.0.1:54510
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Connected to peer at ('127.0.0.1', 54508).
P2P client listening on 127.0.0.1:54511
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Connected to peer at ('127.0.0.1', 54508).
P2P client listening on 127.0.0.1:54512
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Connected to peer at ('127.0.0.1', 54508).
P2P client listening on 127.0.0.1:54513
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Connected to peer at ('127.0.0.1', 54508).
P2P client listening on 127.0.0.1:54514
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Connected to peer at ('127.0.0.1', 54508).
P2P client listening on 127.0.0.1:54515
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Connected to peer at ('127.0.0.1', 54508).
P2P client listening on 127.0.0.1:54516
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54507).
[INFO] Connected to peer at ('127.0.0.1', 54508).
[INFO] Incoming P2P connection from ('127.0.0.1', 32984)
[INFO] Incoming P2P connection from ('127.0.0.1', 35226)
[INFO] Connected to peer at ('127.0.0.1', 54509).
[INFO] Incoming P2P connection from ('127.0.0.1', 35234)
[INFO] Incoming P2P connection from ('127.0.0.1', 35246)
[INFO] Incoming P2P connection from ('127.0.0.1', 55026)
[INFO] Connected to peer at ('127.0.0.1', 54509).
[INFO] Incoming P2P connection from ('127.0.0.1', 35254)
[INFO] Incoming P2P connection from ('127.0.0.1', 32990)
[INFO] Incoming P2P connection from ('127.0.0.1', 35256)
[INFO] Incoming P2P connection from ('127.0.0.1', 32998)
[INFO] Incoming P2P connection from ('127.0.0.1', 35268)
[INFO] Incoming P2P connection from ('127.0.0.1', 32954)
[INFO] Connected to peer at ('127.0.0.1', 54509).
[INFO] Incoming P2P connection from ('127.0.0.1', 32966)
[INFO] Incoming P2P connection from ('127.0.0.1', 35278)
[INFO] Incoming P2P connection from ('127.0.0.1', 33006)
[INFO] Incoming P2P connection from ('127.0.0.1', 33016)
[INFO] Incoming P2P connection from ('127.0.0.1', 33026)
[INFO] Incoming P2P connection from ('127.0.0.1', 33038)
[INFO] Connected to peer at ('127.0.0.1', 54509).
[INFO] Incoming P2P connection from ('127.0.0.1', 32972)
[INFO] Connected to peer at ('127.0.0.1', 54510).
[INFO] Incoming P2P connection from ('127.0.0.1', 35476)
[INFO] Connected to peer at ('127.0.0.1', 54509).[INFO] Incoming P2P connection from ('127.0.0.1', 32980)

[INFO] Connected to peer at ('127.0.0.1', 54510).
==================== short test summary info =====================
FAILED tests/client_test.py::test_node_sockets - assert 7 == (10 - 1)
================== 1 failed, 1 passed in 15.74s ==================
```

### 2. `node_test.py`
```
python3 -m pytest tests/node_test.py
```
```
========================================================================== test session starts ===========================================================================
platform linux -- Python 3.8.10, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/yc3387/project-fat-cat
collected 3 items                                                                                                                                                        

tests/node_test.py F[INFO] Connected to peer at ('127.0.0.1', 54462).
[INFO] Incoming P2P connection from ('127.0.0.1', 40694)
F.                                                                                                                                             [100%]

================================================================================ FAILURES ================================================================================
_____________________________________________________________________________ test_two_nodes _____________________________________________________________________________

    def test_two_nodes():
        app_send1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        app_send2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        base_port = random.randint(49152, 65535)
        tracker = Tracker('127.0.0.1', base_port, 'tracker')
        node1 = Node(
            log_filepath="node_1",
            p2p_addr=('127.0.0.1', base_port + 1),
            node_addr=('127.0.0.1', base_port + 3),
            tracker_addr=('127.0.0.1', base_port))
        node2 = Node(
            log_filepath="node_2",
            p2p_addr=('127.0.0.1', base_port + 2),
            node_addr=('127.0.0.1', base_port + 4),
            tracker_addr=('127.0.0.1', base_port))
    
        time.sleep(3)
        assert node1._get_num_peers() == 1
        assert node2._get_num_peers() == 1
    
        app_send1.connect(('127.0.0.1', base_port + 3))
        app_send2.connect(('127.0.0.1', base_port + 4))
    
        # base blocks in both peers
        database = [b"hello", b"goodbye", b"test"]
        with open('public_key.pem', 'rb') as public_key_file:
            public_key_bytes = public_key_file.read()
        public_key_msg = Message('K', public_key_bytes).pack()
        for data in database:
            signature = sign_data(data, 'private_key.pem')
            msg = Message('A', public_key_msg + signature + data)
            app_send1.sendall(msg.pack())
            app_send2.sendall(msg.pack())
    
        # time.sleep(3)
        # assert node1.bc.isValid()
        # assert node2.bc.isValid()
        # assert len(node1.bc.chain) == len(database)
        # assert len(node2.bc.chain) == len(database)
    
        # add some new blocks in peer1's chain
        chain1_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5"]
        for data in chain1_new:
            signature = sign_data(data, 'private_key.pem')
            msg = Message('A', public_key_msg + signature + data)
            app_send1.sendall(msg.pack())
    
        # send a new post to node2
        post = b"post block"
        signature = sign_data(post, 'private_key.pem')
        msg = Message('A', public_key_msg + signature + post)
        app_send2.sendall(msg.pack())
    
        time.sleep(3)
        assert node1.bc.isValid()
        assert node2.bc.isValid()
>       assert len(node1.bc.chain) == len(database) + len(chain1_new) + 1
E       AssertionError: assert 4 == ((3 + 5) + 1)
E        +  where 4 = len([<src.blockchain.blockchain.Block object at 0x7f2884ab2910>, <src.blockchain.blockchain.Block object at 0x7f2884a55d60>, <src.blockchain.blockchain.Block object at 0x7f2884a621f0>, <src.blockchain.blockchain.Block object at 0x7f2884a502b0>])
E        +    where [<src.blockchain.blockchain.Block object at 0x7f2884ab2910>, <src.blockchain.blockchain.Block object at 0x7f2884a55d60>, <src.blockchain.blockchain.Block object at 0x7f2884a621f0>, <src.blockchain.blockchain.Block object at 0x7f2884a502b0>] = <src.blockchain.blockchain.Blockchain object at 0x7f2884ab2490>.chain
E        +      where <src.blockchain.blockchain.Blockchain object at 0x7f2884ab2490> = <src.node.Node object at 0x7f2884ab2220>.bc
E        +  and   3 = len([b'hello', b'goodbye', b'test'])
E        +  and   5 = len([b'chain1_1', b'chain1_2', b'chain1_3', b'chain1_4', b'chain1_5'])

tests/node_test.py:73: AssertionError
-------------------------------------------------------------------------- Captured stdout call --------------------------------------------------------------------------
P2P client listening on 127.0.0.1:53772
[INFO] Connected to tracker.
P2P client listening on 127.0.0.1:53773
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 53772).
[INFO] Incoming P2P connection from ('127.0.0.1', 52254)
[Blockchain] Add new block[Blockchain] Add new block

[Blockchain] Add new block[Blockchain] Add new block

[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
____________________________________________________________________________ test_multi_nodes ____________________________________________________________________________

    def test_multi_nodes():
        base_port = random.randint(49152, 65000)
        tracker = Tracker('127.0.0.1', base_port, 'tracker')
        num_nodes = 7
        app_socks = []
        nodes = []
        for i in range(num_nodes):
            app_socks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            nodes.append(Node(
                log_filepath=f"node_{i}",
                p2p_addr=('127.0.0.1', base_port + 1 + i * 2),
                node_addr=('127.0.0.1', base_port + 2 + i * 2),
                tracker_addr=('127.0.0.1', base_port)))
            app_socks[i].connect(('127.0.0.1', base_port + 2 + i * 2))
            time.sleep(i)
>           assert nodes[i]._get_num_peers() == i
E           assert 1 == 4
E            +  where 1 = <bound method Worker._get_num_peers of <src.node.Node object at 0x7f28841f8c10>>()
E            +    where <bound method Worker._get_num_peers of <src.node.Node object at 0x7f28841f8c10>> = <src.node.Node object at 0x7f28841f8c10>._get_num_peers

tests/node_test.py:95: AssertionError
-------------------------------------------------------------------------- Captured stdout call --------------------------------------------------------------------------
P2P client listening on 127.0.0.1:54458
[INFO] Connected to tracker.
P2P client listening on 127.0.0.1:54460
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54458).
[INFO] Incoming P2P connection from ('127.0.0.1', 39446)
P2P client listening on 127.0.0.1:54462
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54458).[INFO] Incoming P2P connection from ('127.0.0.1', 40484)

[INFO] Connected to peer at ('127.0.0.1', 54460).
[INFO] Incoming P2P connection from ('127.0.0.1', 46432)
P2P client listening on 127.0.0.1:54464
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54458).
[INFO] Incoming P2P connection from ('127.0.0.1', 40490)
[INFO] Connected to peer at ('127.0.0.1', 54460).
[INFO] Connected to peer at ('127.0.0.1', 54462).[INFO] Incoming P2P connection from ('127.0.0.1', 58056)

[INFO] Incoming P2P connection from ('127.0.0.1', 46442)
P2P client listening on 127.0.0.1:54466
[INFO] Connected to tracker.
[INFO] Connected to peer at ('127.0.0.1', 54458).
[INFO] Incoming P2P connection from ('127.0.0.1', 40498)
[INFO] Connected to peer at ('127.0.0.1', 54460).
[INFO] Incoming P2P connection from ('127.0.0.1', 46458)
======================================================================== short test summary info =========================================================================
FAILED tests/node_test.py::test_two_nodes - AssertionError: assert 4 == ((3 + 5) + 1)
FAILED tests/node_test.py::test_multi_nodes - assert 1 == 4
====================================================================== 2 failed, 1 passed in 27.60s ======================================================================
```

### 3. `tracker_test.py`
```
python3 -m pytest tests/tracker_test.py
```
```
======================= test session starts ========================
platform linux -- Python 3.8.10, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/yc3387/project-fat-cat
collected 1 item                                                   

tests/tracker_test.py .                                      [100%]

======================== 1 passed in 3.11s =========================
```

### 4. `worker_test.py`
```
python3 -m pytest tests/worker_test.py
```
```
====================== test session starts =======================
platform linux -- Python 3.8.10, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/yc3387/project-fat-cat
collected 1 item                                                 

tests/worker_test.py F                                     [100%]

============================ FAILURES ============================
___________________ test_merge_longer_chain[0] ___________________

iteration = 0

    @pytest.mark.parametrize("iteration", range(1))
    def test_merge_longer_chain(iteration):
        sock1, sock2 = socket.socketpair()
        node1 = Worker(enable_mining=True, name="node1", log_filepath="node1")
        node2 = Worker(enable_mining=True, name="node2", log_filepath="node2")
    
        # base blocks in both peers
        database = [b"hello", b"goodbye", b"test"]
        with open('public_key.pem', 'rb') as public_key_file:
            public_key_bytes = public_key_file.read()
        for data in database:
            signature = sign_data(data, 'private_key.pem')
            node1._new_pending_block(signature=signature, public_key_bytes=public_key_bytes, data=data)
            node2._new_pending_block(signature=signature, public_key_bytes=public_key_bytes, data=data)
    
        # time.sleep(1)
    
        # add some new blocks in peer1's chain
        chain1_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5"]
        for data in chain1_new:
            signature = sign_data(data, 'private_key.pem')
            node1._new_pending_block(signature=signature, public_key_bytes=public_key_bytes, data=data)
    
        # wait for peer1 mining complete
        # time.sleep(1)
    
        # connect peer1 and peer2
        node1._peer_join(sock1)
        node2._peer_join(sock2)
    
        # send a new post to node2
        post = b"post block"
        signature = sign_data(post, 'private_key.pem')
        node2._new_pending_block(signature=signature, public_key_bytes=public_key_bytes, data=post)
    
        """
        both start mining this block of post at the same time
        peer2 will recieve the post directly, and peer1 will recieve it through peer2's forwarding
        case1: peer2 found a valid block and forward it to peer1:
          => unattachable, pull the whole chain
          => peer1's local chain is longer than peer2's remote chain
          => reject to merge
        case2: peer1 found a valid block and forward it to peer2:
          => unattachable, pull the whole chain
          => peer2's local chain is shorter than peer1's remote chain
          => merged and synchronized successfully
        """
        time.sleep(10)
        # print(len(database) + len(chain1_new) + 1)
        # print(len(node1.bc.chain))
        # print(len(node2.bc.chain))
        # print(node1.bc.isValid())
        # print(node2.bc.isValid())
        # print(node1.bc)
        # print("----------------------------------")
        # print(node2.bc)
        assert node1.bc.isValid()
        assert node2.bc.isValid()
>       assert len(node1.bc.chain) == len(database) + len(chain1_new) + 1
E       AssertionError: assert 8 == ((3 + 5) + 1)
E        +  where 8 = len([<src.blockchain.blockchain.Block object at 0x7ff9f5778460>, <src.blockchain.blockchain.Block object at 0x7ff9f571a2b0...blockchain.blockchain.Block object at 0x7ff9f571a130>, <src.blockchain.blockchain.Block object at 0x7ff9f571a5e0>, ...])
E        +    where [<src.blockchain.blockchain.Block object at 0x7ff9f5778460>, <src.blockchain.blockchain.Block object at 0x7ff9f571a2b0...blockchain.blockchain.Block object at 0x7ff9f571a130>, <src.blockchain.blockchain.Block object at 0x7ff9f571a5e0>, ...] = <src.blockchain.blockchain.Blockchain object at 0x7ff9f576eee0>.chain
E        +      where <src.blockchain.blockchain.Blockchain object at 0x7ff9f576eee0> = <src.blockchain.worker.Worker object at 0x7ff9f5824760>.bc
E        +  and   3 = len([b'hello', b'goodbye', b'test'])
E        +  and   5 = len([b'chain1_1', b'chain1_2', b'chain1_3', b'chain1_4', b'chain1_5'])

tests/worker_test.py:75: AssertionError
---------------------- Captured stdout call ----------------------
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
[Blockchain] Add new block
==================== short test summary info =====================
FAILED tests/worker_test.py::test_merge_longer_chain[0] - AssertionError: assert 8 == ((3 + 5) + 1)
======================= 1 failed in 10.68s =======================
```

## Test Coverage
The tests cover the following key aspects:
- Socket communication between nodes and the tracker.
- Blockchain operations such as block creation, mining, and synchronization.
- Network dynamics including node registration, heartbeat updates, and peer list management.
- Integration of cryptographic functions within node operations.

## Known Issues & Limitations
- Network latency and asynchronous operations can lead to non-deterministic test outcomes, particularly in network synchronization tests.
- The system assumes a reliable network environment; network partitions are not simulated in the current test suite.

