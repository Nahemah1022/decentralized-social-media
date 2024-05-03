import pytest
import socket
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.blockchain import Worker
from src.crypto import sign_data, generate_rsa_key_pair

@pytest.fixture(scope="session")
def generate_keys():
    if not os.path.exists('public_key.pem') or not os.path.exists('private_key.pem'):
        generate_rsa_key_pair()

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
    assert len(node1.bc.chain) == len(database) + len(chain1_new) + 1
    assert len(node2.bc.chain) == len(database) + len(chain1_new) + 1
    node1.stop()
    node2.stop()

if __name__ == '__main__':
    test_merge_longer_chain(1)
