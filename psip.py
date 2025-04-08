import logging
from exceptions import ParseFailed, TypeMismatch, StackUnderflow
from utils import is_num, is_int
import math
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

op_stack = []   # type: ignore
dict_stack = [] # type: ignore
dict_stack.append({}) # global dict 

def repl():
    while True:
        user_input = input("REPL> ")
        if user_input.lower() == "quit":
            break
        process_input(user_input)
        logging.debug(f"Operand Stack: {op_stack}")

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
    
def add_operation():
    if len(op_stack) >= 2 and is_num(op_stack[-1]) and is_num(op_stack[-2]):
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op1 + op2 
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation add")
    
def sub_operation():
    if len(op_stack) >= 2 and is_num(op_stack[-1]) and is_num(op_stack[-2]):
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op2 - op1  # rev bc postfix, so { 1 2 sub } == -1
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation add")

def div_operation():
    if len(op_stack) >= 2 and is_num(op_stack[-1]) and is_num(op_stack[-2]):
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if op1 == 0:
            raise DivByZero("dividing by zero is invalid")
        res = op2 / op1  # rev bc postfix, so { 1 2 div } == 1 / 2
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation div")

def idiv_operation():
    if len(op_stack) >= 2 and is_int(op_stack[-1]) and is_int(op_stack[-2]):
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if op1 == 0:
            raise DivByZero("dividing by zero is invalid")
        res = op2 // op1  # rev bc postfix, so { 1 2 div } == 1 // 2
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation div")

def mod_operation():
    if len(op_stack) >= 2 and is_int(op_stack[-1]) and is_int(op_stack[-2]):
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if op1 == 0:
            raise DivByZero("dividing by zero is invalid")
        res = op2 % op1  # rev bc postfix, so { 1 2 mod } == 1 % 2 
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation mod")

def abs_operation():
    if len(op_stack) >= 1 and is_num(op_stack[-1]):
        op_stack[-1] = abs(op_stack[-1])
    else:
        raise StackUnderflow("not enough operands for operation abs")

def neg_operation():
    if len(op_stack) >= 1 and is_num(op_stack[-1]):
        op_stack[-1] = -op_stack[-1]
    else:
        raise StackUnderflow("not enough operands for operation neg")

def ceil_operation():
    if len(op_stack) >= 1 and is_num(op_stack[-1]):
        op_stack[-1] = math.ceil(op_stack[-1])
    else:
        raise StackUnderflow("not enough operands for operation ceil")

def floor_operation():
    if len(op_stack) >= 1 and is_num(op_stack[-1]):
        op_stack[-1] = math.floor(op_stack[-1])
    else:
        raise StackUnderflow("not enough operands for operation floor")

def round_operation():
    if len(op_stack) >= 1 and is_num(op_stack[-1]):
        op_stack[-1] = round(op_stack[-1])
    else:
        raise StackUnderflow("not enough operands for operation round")

def sqrt_operation():
    if len(op_stack) >= 1 and is_num(op_stack[-1]):
        op_stack[-1] = math.sqrt(op_stack[-1])
    else:
        raise StackUnderflow("not enough operands for operation sqrt")

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


def lookup_in_dictionary(input):
    top_dict = dict_stack[-1] # current scope
    if input in top_dict:
        value = top_dict[input]
        if callable(value): # checks if python func
            value()
        elif isinstance(value, list):
            for item in value:
                process_input(item)
        else:
            op_stack.append(value)
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
    process_name_constant
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