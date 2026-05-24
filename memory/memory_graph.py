class MemoryGraph:
    def __init__(self):
        self.nodes = []

    def add(self, item):
        self.nodes.append(item)

    def query(self):
        return self.nodes[-10:]
