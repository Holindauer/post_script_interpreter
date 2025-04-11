def is_num(x) -> bool:
    return isinstance(x, (int, float))

def is_int(x) -> bool:
    return isinstance(x, int)

def is_bool(x) -> bool:
    return isinstance(x, bool)

def is_string(x) -> bool:
    return isinstance(x, str)

def is_mutable_string(x) -> bool:
    return isinstance(x, MutableString)

class MutableString:
    """Python strings but mutable"""
    def __init__(self, string):
        assert isinstance(string, str), "must be string"
        self.string = string
    def putinterval(self, index, string):
        """performs putinterval operation on string"""
        self.string = self.string[:index] + string + self.string[index+len(string):]
        return self.string
    def __repr__(self):
        return self.string
        
class DictWithCapacity(dict):
    def __init__(self, capacity: int):
        self.capacity = capacity
        super().__init__()

    def __setitem__(self, key, value):
        if len(self) >= self.capacity:
            raise Exception("dict is full")
        super().__setitem__(key, value)