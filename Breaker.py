class CircuitBreaker:
    def __init__(self):
        self.is_open = False
    def open(self):
        self.is_open = True
    def close(self):
        self.is_open = False
    def get_is_open(self):
        return self.is_open