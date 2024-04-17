# CSEE 4119 Spring 2024, Class Project 
# A Decentralized Social Network Application

## Design Overview
### Architecture
- A decentralized blockchain, which is permissionless that allows anyone to participate in the network without prior approval.
- Uses a Proof of Stake (PoS) mechanism to ensure network security and consensus.
- Block structure: 
    - Header: includes the block version, previous block hash, timestamp, Merkle tree root hash, and nonce.
    - Body: consists of multiple transactions, each representing different types of user interactions like posts, likes, comments, and follows.

### Cryptography
- Hash functions: uses SHA-256 to generate cryptographic hashes for blocks and transactions.
- Signature scheme: uses ECDSA (Elliptic Curve Digital Signature Algorithm) to verify the identity of message senders, ensure data integrity and non-repudiation.

## Peer-to-Peer (P2P) Protocol
### Network Structure
- A tracker: maintains an updated list of peers in the network, which is dynamically updated when peers join or leave the network.
- Node types (at leaset 3 peers)
    - Full nodes: maintain a complete copy of the blockchain, validate blocks and transactions, and participate in the consensus process.
    - Light nodes: hold essential data and rely on full nodes for additional information and validation services.

### Network Mechanism
- Peer discovery: utilizes a DHT (Distributed Hash Table) for efficient peer discovery and management.
- Message broadcast: implements gossip protocols to propagate transactions and blocks across the network effectively.
- Data syncing: nodes initially perform a complete sync of the blockchain from other peers and continuously receive new blocks and transactions.
- Handling forks: implements fork resolution mechanisms to maintain a consistent view of the ledger among all participants.

## Enhanced Functionalities [TBD]
- Dynamic adjustment of mining difficulty based on the available computation power
- Verify transactions using Merkle Tree

## Demo Application Design
### Key Functionalities
- User registration and authentication: users can create and manage blockchain-based identities.
- Content creation: users can post content, which is recorded as transactions on the blockchain.
- Social interactions: the ability to follow other users, like and comment on posts.
### Tech Stacks [TBD]
- Front-end
    - HTML
    - CSS
    - React
- Back-End
    - Python
