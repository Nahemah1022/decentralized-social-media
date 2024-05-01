from .blockchain import Worker
from .p2p import P2PClient

class Node(Worker):
    def __init__(self, p2p_addr, tracker_addr, app_sockets=None, enable_mining=True, name="default", log_filepath=None):
        super().__init__(app_sockets, enable_mining, name, log_filepath)
        self.p2p_client = P2PClient(p2p_addr, tracker_addr, self._peer_join, self._peer_leave)

    def stop(self):
        self.p2p_client.stop()
        super().stop()
