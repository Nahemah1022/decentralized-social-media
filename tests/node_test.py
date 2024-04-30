import pytest
import socket
import time

from src import Node, sign_data, Message

def test_merge_longer_chain():
    app_send1, app_recv1 = socket.socketpair()
    app_send2, app_recv2 = socket.socketpair()
    sock1, sock2 = socket.socketpair()
    node1 = Node([app_recv1], enable_mining=True, name="node1")
    node2 = Node([app_recv2], enable_mining=True, name="node2")

    # base blocks in both peers
    database = [b"hello", b"goodbye", b"test"]
    for data in database:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', signature + data)
        app_send1.sendall(msg.pack())
        app_send2.sendall(msg.pack())
    
    # time.sleep(1)

    # add some new blocks in peer1's chain
    chain1_new = [b"chain1_1", b"chain1_2", b"chain1_3", b"chain1_4", b"chain1_5"]
    for data in chain1_new:
        signature = sign_data(data, 'private_key.pem')
        msg = Message('A', signature + data)
        app_send1.sendall(msg.pack())

    # wait for peer1 mining complete 
    # time.sleep(1)

    # connect peer1 and peer2
    node1._peer_join(sock1)
    node2._peer_join(sock2)

    # send a new post to node2
    post = b"post block"
    signature = sign_data(post, 'private_key.pem')
    msg = Message('A', signature + post)
    app_send2.sendall(msg.pack())

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
    time.sleep(3)
    # assert node2.bc.isValid()
    # assert len(node2.bc.chain) == len(database) + len(chain1_new) + 1
    print(len(database) + len(chain1_new) + 1)
    print(len(node1.bc.chain))
    print(len(node2.bc.chain))
    print(node1.bc.isValid())
    print(node2.bc.isValid())
    node2.bc.print()
    print("----------------------------------")
    node1.bc.print()
    node1.stop()
    node2.stop()

if __name__ == '__main__':
    test_merge_longer_chain()
