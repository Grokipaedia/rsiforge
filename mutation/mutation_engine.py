class MutationEngine:
    def propose(self, state):
        return {
            "change": "reverse_output",
            "expected_gain": 0.1
        }
