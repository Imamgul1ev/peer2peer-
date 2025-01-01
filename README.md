# P2P Network with Rendezvous Server

This project demonstrates a Peer-to-Peer (P2P) communication system using a central rendezvous server to enable peer discovery. It uses UDP sockets for exchanging messages between peers.

## How It Works

### Rendezvous Server
The **Rendezvous Server** acts as a central point for peer discovery:
- It listens for incoming sync requests from peers.
- Maintains a list of all connected peers (`neighbours`).
- Shares this list with newly connected peers to help them discover and communicate with others.

### Peer (P2P Node)
The **Peer** interacts with the rendezvous server and other peers:
- It sends a sync request to the rendezvous server to register itself and obtain the list of neighbors.
- After synchronization, the peer can communicate with other peers by sending direct messages (unicast) or broadcasting to all known peers.
