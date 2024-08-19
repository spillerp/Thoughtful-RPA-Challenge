class DataStorage:
    def __init__(self):
        self.data = {}

    def set_data(self, key: str, value):
        self.data[key] = value
        return

    def get_data(self, key: str, default=None):
        return self.data.get(key, default)