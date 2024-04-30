import threading

class AtomicBool:
    def __init__(self, initial=True):
        self.value = initial
        self.lock = threading.Lock()
    
    def set(self, val):
        with self.lock:
            self.value = val
    
    def get(self):
        with self.lock:
            return self.value