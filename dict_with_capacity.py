class DictWithCapacity(dict):
    def __init__(self, capacity: int):
        self.capacity = capacity
        super().__init__()

    def __setitem__(self, key, value):
        if len(self) >= self.capacity:
            raise Exception("dict is full")
        super().__setitem__(key, value)