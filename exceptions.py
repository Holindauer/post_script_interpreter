class ParseFailed(Exception):
    """ Exception while parsing """ 
    def __init__(self, message):
        super().__init__(message)

class TypeMismatch(Exception):
    """ Exception with types of operators and operands """ 
    def __init__(self, message):
        super().__init__(message)

class DivByZero(Exception):
    """ Exception when dividing by zero """ 
    def __init__(self, message):
        super().__init__(message)