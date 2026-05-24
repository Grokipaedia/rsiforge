class TruthMetric:
    def score(self, input_data, output):
        return len(output) / (len(input_data) + 1)
