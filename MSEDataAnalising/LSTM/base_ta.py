
class IndicatorStrategy:
    def calculate(self, data):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def generate_signals(self, data):
        raise NotImplementedError("This method should be overridden by subclasses.")