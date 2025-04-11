import logging
from exceptions import ParseFailed, TypeMismatch, StackUnderflow, DivByZero
from utils import is_num, is_int, is_bool, is_list, is_mutable_string, DictWithCapacity, MutableString
import math
from typing import Callable
import re

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

op_stack = []   # type: ignore
dict_stack = [] # type: ignore
dict_stack.append({}) # global dict 

def repl():
    while True:
        user_input = lexer(input("REPL> "))
        for token in user_input:
            if token.lower() == "quit":
                break
            process_input(token)
            logging.debug(f"Operand Stack: {op_stack}")
            logging.debug(f"Dictionary Stack: {dict_stack}")
            logging.info(f"\n\nOperand Stack: {op_stack}")
            logging.info(f"Dictionary Stack: {dict_stack}")

def lexer(input):
    """regex to get tokens from () {} or atomic whitespace seperated tokens"""
    return re.findall(r'(\(.*?\)|\{.*?\}|\S+)', input)

def def_operation():
    if len(op_stack) >= 2:
        value = op_stack.pop()
        name = op_stack.pop()
        if isinstance(name, str) and name.startswith("/"):
            key = name[1:]
            dict_stack[-1][key] = value
        else: 
            op_stack.append(name)
            op_stack.append(value)
    else:
        raise TypeMismatch("not enough operands for operation add")

def dict_operation():
    if len(op_stack) >= 1 and is_int(op_stack[-1]):
        capacity = op_stack.pop()
        new_scope = DictWithCapacity(capacity)
        op_stack.append(new_scope)
    else:
        raise TypeMismatch("integer capacity must be provided")

def begin_operation():
    if len(op_stack) >= 1 and isinstance(op_stack[-1], DictWithCapacity):
        new_scope = op_stack.pop()
        dict_stack.append(new_scope)
    else:
        raise TypeMismatch("top stack element must be dictionary to begin")

def end_dict_operation():
    if len(dict_stack) > 1:
        dict_stack.pop()
    else:
        raise StackUnderflow("cannot erase global scope")

def length_operation():

    if not (len(op_stack) >= 1):
        raise StackUnderflow("not enough operands for operation length")

    is_dict = isinstance(op_stack[-1], dict)
    is_dict_with_capacity = isinstance(op_stack[-1], DictWithCapacity)
    if is_dict or is_dict_with_capacity:
        op_stack.append(len(op_stack[-1]))
    elif is_mutable_string(op_stack[-1]):
        op_stack.append(len(op_stack[-1].string))
    else: 
        raise TypeMismatch("top stack element must be collection to length")

def maxlength_operation():
    if not (len(op_stack) >= 1):
        raise StackUnderflow("not enough operands for operation length")
    if  isinstance(op_stack[-1], DictWithCapacity): # only user defined dictationaries have capacity
        op_stack.append(op_stack[-1].capacity)
    else: 
        raise TypeMismatch("top stack element must be collection to maxlength")


def div(x, y):
    return x / y
def idiv(x, y):
    return x // y
def mod(x, y):
    return x % y

def binary_operation(op: Callable):
    if len(op_stack) >= 2 and is_num(op_stack[-1]) and is_num(op_stack[-2]):
        op1 = op_stack.pop()
        if op1 == 0 and (op in [div, idiv, mod]):
            raise DivByZero("dividing by zero is invalid")
        op2 = op_stack.pop()
        res = op(op2, op1)
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation binary")
        
def unary_operation(op: Callable):
    if not len(op_stack) >= 1:
        raise StackUnderflow(f"not enough operands for operation {op.__name__}")
    elif is_num(op_stack[-1]):
        op_stack[-1] = op(op_stack[-1])
    elif is_bool(op_stack[-1]):
        op_stack[-1] = op(op_stack[-1])
    else:
        raise TypeMismatch("top stack element must be number to apply operation")

def div_operation():
    binary_operation(div)

def idiv_operation():
    binary_operation(idiv)

def mod_operation():
    binary_operation(mod)
    
def add_operation():
    binary_operation(lambda x, y: x + y)
    
def sub_operation():
    binary_operation(lambda x, y: x - y)

def abs_operation():
    unary_operation(abs)

def neg_operation():
    unary_operation(lambda x: -x)

def ceil_operation():
    unary_operation(math.ceil)

def floor_operation():
    unary_operation(math.floor)

def round_operation():
    unary_operation(round)

def sqrt_operation():
    unary_operation(math.sqrt)

def ne_operation():
    binary_operation(lambda x, y: x != y)

def eq_operation():
    binary_operation(lambda x, y: x == y)

def ge_operation():
    binary_operation(lambda x, y: x >= y)

def gt_operation():
    binary_operation(lambda x, y: x > y)

def le_operation():
    binary_operation(lambda x, y: x <= y)

def lt_operation():
    binary_operation(lambda x, y: x < y)

def and_operation():
    binary_operation(lambda x, y: x and y)

def not_operation():
    unary_operation(lambda x: not x)

def or_operation():
    binary_operation(lambda x, y: x or y)

def true_operation():
    op_stack.append(True)

def false_operation():
    op_stack.append(False)

def dup_operation():
    """duplicates the top stack element"""
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        op_stack.append(op1)
        op_stack.append(op1)
    else:
        raise StackUnderflow("not enough operands for operation dup")

def exch_operation():
    """Exchanges top two stack elements"""
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op1)
        op_stack.append(op2)
    else:
        raise StackUnderflow("not enough operands for operation exch")

def pop_operation():
    """rm top stack element"""
    if len(op_stack) >= 1:
        op_stack.pop()
    else:
        raise StackUnderflow("not enough operands for operation pop")

def clear_operation():
    op_stack.clear()

def pop_and_print():
    if(len(op_stack) >= 1):
        op1 = op_stack.pop()
        print(op1)
    else:
        raise TypeMismatch("Stack is empty! nothin to print")
    
def count_operation():
    stack_len = len(op_stack)
    op_stack.append(stack_len)

def copy_operation():
    """copies the top n elements"""
    if len(op_stack) >= 1:
        n = op_stack[-1]
        if len(op_stack) - 1 >= n:
            elements_to_copy = op_stack[:-1][::-1][:n+1][::-1]
            op_stack.pop()
            op_stack.extend(elements_to_copy)
    else:
        raise StackUnderflow("not enough operands for operation copy")
    
def get_operation():
    """
    returns ascii code of the selected index of a str
    string index get
    """
    if not (len(op_stack) >= 2):
        raise StackUnderflow("not enough operands for operation get")
    elif is_mutable_string(op_stack[-2]) and is_int(op_stack[-1]):
        index = op_stack.pop()
        string = op_stack.pop().string
        ascii = ord(string[index])
        op_stack.append(ascii)
    else:
        raise TypeMismatch("Wrong operands for operation get")

def getinterval_operation():
    if not (len(op_stack) >= 3):
        raise StackUnderflow("not enough operands for operation getinterval")
    elif is_mutable_string(op_stack[-3]) and is_int(op_stack[-2]) and is_int(op_stack[-1]):
        end = op_stack.pop()
        start = op_stack.pop()
        string = op_stack.pop().string
        op_stack.append(string[start:end+1])
    else:
        raise TypeMismatch("Wrong operands for operation getinterval")

def put_interval_operation():
    """ string1 index string2 putinterval"""
    if not (len(op_stack) >= 3):
        raise StackUnderflow("not enough operands for operation putinterval")
    elif is_mutable_string(op_stack[-3]) and is_int(op_stack[-2]) and is_mutable_string(op_stack[-1]):
        string2 = op_stack.pop()  
        index = op_stack.pop()    
        string1 = op_stack.pop()  
        
        # Modify string1 in place
        string1.putinterval(index, string2.string)
    else:
        raise TypeMismatch("Wrong operands for operation putinterval")
            
def if_operation():
    if not (len(op_stack) >= 2):
        raise StackUnderflow("not enough operands for operation if")
    elif is_list(op_stack[-1]) and is_bool(op_stack[-2]):
        process = op_stack.pop()
        boolean = op_stack.pop()
        if boolean:
            for item in process:
                process_input(item)
    else:
        raise TypeMismatch("Wrong operands for operation if")

def ifelse_operation():
    pass

def for_operation():
    pass

def repeat_operation():
    pass

def quit_operation():
    pass


# add arithmetic operations to the global dictionary/scope
dict_stack[-1]["add"] = add_operation
dict_stack[-1]["def"] = def_operation
dict_stack[-1]["sub"] = sub_operation
dict_stack[-1]["div"] = div_operation
dict_stack[-1]["idiv"] = idiv_operation
dict_stack[-1]["mod"] = mod_operation
dict_stack[-1]["abs"] = abs_operation
dict_stack[-1]["neg"] = neg_operation
dict_stack[-1]["ceil"] = ceil_operation
dict_stack[-1]["floor"] = floor_operation
dict_stack[-1]["round"] = round_operation
dict_stack[-1]["sqrt"] = sqrt_operation

# stack manipulation operations
dict_stack[-1]["dup"] = dup_operation
dict_stack[-1]["exch"] = exch_operation
dict_stack[-1]["pop"] = pop_operation
dict_stack[-1]["clear"] = clear_operation
dict_stack[-1]["count"] = count_operation
dict_stack[-1]["copy"] = copy_operation

# input operations
dict_stack[-1]["="] = pop_and_print

# dictionary operations
dict_stack[-1]["dict"] = dict_operation
dict_stack[-1]["begin"] = begin_operation
dict_stack[-1]["end"] = end_dict_operation
dict_stack[-1]["length"] = length_operation
dict_stack[-1]["maxlength"] = maxlength_operation

# boolean operations
dict_stack[-1]["ne"] = ne_operation
dict_stack[-1]["eq"] = eq_operation
dict_stack[-1]["ge"] = ge_operation
dict_stack[-1]["gt"] = gt_operation
dict_stack[-1]["le"] = le_operation
dict_stack[-1]["lt"] = lt_operation
dict_stack[-1]["or"] = or_operation
dict_stack[-1]["not"] = not_operation
dict_stack[-1]["true"] = true_operation
dict_stack[-1]["false"] = false_operation

# TODO String operations
dict_stack[-1]["length"] = length_operation
dict_stack[-1]["get"] = get_operation
dict_stack[-1]["getinterval"] = getinterval_operation
dict_stack[-1]["putinterval"] = put_interval_operation

# TODO control flow operations
dict_stack[-1]["if"] = if_operation

# TODO IO operations

def lookup_in_dictionary(input, dynamic_scoping=True):

    if dynamic_scoping:
        for scope in dict_stack[::-1]:
            if input in scope:
                value = scope[input]
                if callable(value): # checks if python func
                    value()
                elif isinstance(value, list):
                    for item in value:
                        process_input(item)
                else:
                    op_stack.append(value)    
                return

    elif not dynamic_scoping:
        raise Exception("Not Implemented Yet")                    
    else:
        raise ParseFailed("input {input} is not in dictionary")

def process_input(user_input):
    try:
        process_constants(user_input)
    except ParseFailed as e:
        logging.debug(e)
        try: 
            lookup_in_dictionary(user_input)
        except Exception as e:
            logging.error(e)

def process_boolean(input):
    logging.debug(f"Input to process_boolean: {input}")
    if input == "true":
        return True
    elif input == "false":
        return False
    else:
        raise ParseFailed("cant parse it into boolean")
    
def process_number(input):
    logging.debug(f"Input to process_number: {input}")
    try:
        float_value = float(input)
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except:
        raise ParseFailed("can't parse this into a number")

def process_code_block(input):
    logging.debug(f"Input to process number: {input}")
    if len(input) >= 2 and input.startswith("{") and input.endswith("}"):
        return input[1:-1].strip().split()
    else:
        raise ParseFailed("can't parse this into the code block")
    
def process_string(input):
    logging.debug(f"Input to process number: {input}")
    if len(input) >= 2 and input.startswith("(") and input.endswith(")"):
        return MutableString(input[1:-1])
    else:
        raise ParseFailed("can't parse this into string")
    
def process_name_constant(input):
    logging.debug(f"Input to process number: {input}")
    if input.startswith("/"):
        return input
    else:
        raise ParseFailed("Can't parse into name constant")

PARSERS = [
    process_boolean,
    process_number,
    process_code_block,
    process_name_constant,
    process_string
]

def process_constants(input):
    for parser in PARSERS:
        try:
            res = parser(input)
            op_stack.append(res)
            return 
        except ParseFailed as e:
            logging.debug(e)
            continue
    raise ParseFailed(f"None of the parsers worked for the input {input}")


if __name__ == "__main__":
    repl()