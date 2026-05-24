class IBA:
    def validate_intent(self, intent):
        forbidden = ["delete_memory", "rewrite_truth"]

        if intent in forbidden:
            return False

        return True
