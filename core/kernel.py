class Kernel:
    def __init__(self):
        self.state = {}
        self.log = []

    def step(self, input_data):
        self.log.append(input_data)
        self.state["last_input"] = input_data
        return {"status": "ok", "echo": input_data}
