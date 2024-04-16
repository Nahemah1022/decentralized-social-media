# CSEE 4119 Spring 2024, Class Project
## Team name: Fat Cat

## Design Overview
### Architecture
- Blockchain Type: We use a permissionless blockchain model, which allows anyone to participate in the network without prior approval.
- Consensus Algorithm: The network implements a Proof of Stake (PoS) mechanism to ensure network security and consensus without the high energy cost of Proof of Work systems.
- Block Structure: Each block contains the following elements:
    - Block Header: Includes the block version, previous block hash, timestamp, Merkle tree root hash, and nonce.
    - Block Body: Consists of multiple transactions, each representing different types of user interactions like posts, likes, comments, and follows.

### Smart Contracts 
- Profile Management: Handles creation and updates to user profiles.
*[__TBC__: This might be more complex than needed if profile updates are simple and don't involve conditional logic or transactions that require decentralization.]*
- Content Interaction: Manages posting, commenting, and liking activities.
*[__TBC__: Consider the necessity of smart contracts here unless you need automated, rule-based interactions for these activities.]*
- Moderation: Facilitates community-driven governance for content moderation.
*[__TBC__: This could be simplified or handled off-chain unless you are specifically testing decentralized governance models.]*

### Cryptography
- Hash Functions: SHA-256 is used for generating cryptographic hashes for blocks and transactions.
- Signature Scheme: ECDSA (Elliptic Curve Digital Signature Algorithm) is used for verifying the identity of message senders, ensuring data integrity and non-repudiation.

## Peer-to-Peer (P2P) Protocol
### Network Structure
- Tracker: A dedicated tracker node is responsible for maintaining an updated list of peers in the network. This list is dynamically updated as peers join or leave the network.
- Node Types
    - Full Nodes: Maintain a complete copy of the blockchain, validate blocks and transactions, and participate in the consensus process.
    - Light Nodes: Hold only essential data and rely on full nodes for additional information and validation services.

### Network Communication
- Peer Discovery: Utilizes a DHT (Distributed Hash Table) for efficient peer discovery and management.
- Message Broadcast: Implements gossip protocols to propagate transactions and blocks across the network effectively.

### Data Distribution
- Data Syncing: Nodes initially perform a complete sync of the blockchain from other peers and continuously receive new blocks and transactions.
- Handling Forks: The protocol implements fork resolution mechanisms to maintain a consistent view of the ledger among all participants.

## Blockchain Functionalities
### Performance and Scalability - Dynamic Mining Difficulty
- Adjustment Algorithm: The mining difficulty is dynamically adjusted based on the total hashing power of the network to maintain a consistent time interval between blocks. This ensures the network remains efficient and secure regardless of fluctuations in the number of miners or their computational power.
*[__TBC__: Implementation: The difficulty adjustment algorithm reviews the average time taken to mine the last N blocks, and adjusts the difficulty level to aim for a target block time, e.g., 10 minutes per block.]*

### Data Integrity and Security - Merkle Tree
- Merkle Trees: Each block uses a Merkle tree to efficiently summarize all the transactions it contains. The Merkle root, a single hash, represents the entire set of transactions and is stored in the block header.
- Verification: When verifying a block, nodes use the Merkle tree to efficiently check whether a transaction is included in the block without needing to check every individual transaction. This speeds up the verification process, especially useful when dealing with blocks that contain a large number of transactions.
*[__TBC__: Essential for integrity but ensure the complexity is justified by the transaction volume and type]*

## Demo Application Design
### Functionalities
- User Registration and Authentication: Users can create and manage their blockchain-based identities.
- Content Creation: Users can post content, which is recorded as transactions on the blockchain.
- Social Interactions: Includes the ability to follow other users, like and comment on posts.
### User Interface
- Front-End: A sleek, responsive web interface that provides a seamless user experience. Built using HTML, CSS, and React.
- Back-End: Manages the application logic, interacts with the blockchain, and handles user requests. Implemented in [XXX].
### Data Handling
- Storage: While transaction data is stored on the blockchain, media files and larger content are stored off-chain with references maintained on-chain.
- Privacy Features: Implements cryptographic techniques to ensure that user data remains private and secure.
*[__TBC__: Ensure this design does not complicate the project beyond the scope. Consider the essential need for off-chain storage in a simple demo application.]*