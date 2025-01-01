import time
import json
import socket
import threading


class Peer:
    """Abstraction of peer features for a P2P network."""

    def __init__(self) -> None:
        self.__buffer_size = 2048
        self.__neighbours = dict()

    def build_reader_socket(self, recv_port) -> None:
        """Initialize the reader socket for receiving messages."""
        self.__sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f'Binding reader socket to port {recv_port}...')
        self.__sock_recv.bind(('0.0.0.0', recv_port))

    def build_writer_socket(self, send_port) -> None:
        """Initialize the writer socket for sending messages."""
        self.__sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f'Binding writer socket to port {send_port}...')
        self.__sock_send.bind(('0.0.0.0', send_port))

    def run_forever(self) -> None:
        """Continuously listen for incoming messages in a separate thread."""
        t = threading.Thread(target=self.__run_forever_job)
        t.start()

    def __run_forever_job(self) -> None:
        while True:
            data, _ = self.__sock_recv.recvfrom(self.__buffer_size)
            if not data:
                continue
            data = data.decode()
            print(f'> Received: {data}')
            self.__logic(data)

    def __logic(self, data):
        """Process incoming messages."""
        try:
            data = json.loads(data)
            if data["type"] == "peer_sync_reply":
                self.__neighbours.update(data["neighbours"])
            elif data["type"] == "peer_data":
                print(f'Payload received: {data["payload"]}')
        except KeyError as e:
            print(f"Warning: Missing key in message - {e}")

    def sync_request(self, message, address):
        """Send a sync request to the rendezvous server."""
        print("Sending sync request...")
        self.unicast(message, address)
        print("Sync request sent.")

    def unicast(self, message, address) -> None:
        """Send a message to a single peer."""
        self.__sock_send.sendto(message.encode('utf-8'), address)

    def broadcast(self, message) -> None:
        """Broadcast a message to all known peers."""
        for node_id, details in self.__neighbours.items():
            address = (details["host"], details["destination_port"])
            self.__sock_send.sendto(message.encode('utf-8'), address)


def main():

    peer_reader_port = 5001 
    peer_writer_port = 5002  
    node_id = 1 
    rendezvous_port = 4003  

    peer = Peer()
    peer.build_reader_socket(peer_reader_port)
    peer.build_writer_socket(peer_writer_port)
    peer.run_forever()

    destination_address = ('localhost', rendezvous_port)
    sync_message = json.dumps({
        "node_id": node_id,
        "destination_port": peer_reader_port,
        "type": "peer_sync_request"
    })
    peer.sync_request(sync_message, destination_address)

    time.sleep(1)

    broadcast_message = json.dumps({
        "node_id": node_id,
        "payload": "Hello from Peer!",
        "type": "peer_data"
    })
    peer.broadcast(broadcast_message)


if __name__ == '__main__':
    main()
