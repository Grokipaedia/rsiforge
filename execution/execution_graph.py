class ExecutionGraph:
    def __init__(self):
        self.edges = []

    def log(self, action, result):
        self.edges.append((action, result))
