import logging
from exceptions import ParseFailed, TypeMismatch, StackUnderflow, DivByZero
from utils import is_num, is_int, is_bool, is_list, is_mutable_string, DictWithCapacity, MutableString, Closure
import math
from typing import Callable
import re

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

op_stack = []       # type: ignore
dict_stack = [{}]   # type: ignore
closures = []       # type: ignore

scoping = "DYNAMIC"


def repl():
    while True:
        user_input = lexer(input("REPL> "))
        for token in user_input:
            if token.lower() == "quit":
                return
            process_input(token)
            logging.debug(f"Operand Stack: {op_stack}")
            logging.debug(f"Dictionary Stack: {dict_stack}")
            logging.info(f"\n\nOperand Stack: {op_stack}")
            # logging.info(f"Dictionary Stack: {dict_stack}")
            # logging.info(f"Closures: {[closure.code_block for closure in closures]}")
            # logging.info(f"Closures Dict Stack: {[closure.dict_stack for closure in closures]}")

def lexer(input):
    """regex to get tokens from () {} or atomic whitespace seperated tokens"""
    return re.findall(r'(\(.*?\)|\{.*?\}|\S+)', input)

def check_op_stack_underflow(expected_length: int, attempted_op: str):
    if len(op_stack) < expected_length:
        raise StackUnderflow(f"not enough operands for operation {attempted_op}")
    
def check_dict_stack_underflow(expected_length: int, attempted_op: str):
    if len(dict_stack) < expected_length:
        raise StackUnderflow(f"not enough dictionaries for operation {attempted_op}")

def def_operation():
    check_op_stack_underflow(2, "def")
    value, name = op_stack.pop(), op_stack.pop()
    if isinstance(name, str) and name.startswith("/"):
        key = name[1:]
        dict_stack[-1][key] = value
    else: 
        op_stack.append(name)
        op_stack.append(value)
        raise TypeMismatch("not enough operands for operation add")

def dict_operation():
    check_op_stack_underflow(1, "dict")
    if is_int(op_stack[-1]):
        capacity = op_stack.pop()
        new_scope = DictWithCapacity(capacity)
        op_stack.append(new_scope)
    else:
        raise TypeMismatch("integer capacity must be provided")     

def begin_operation():
    check_op_stack_underflow(1, "begin")
    if isinstance(op_stack[-1], DictWithCapacity):
        new_scope = op_stack.pop()
        dict_stack.append(new_scope)
    else:
        raise TypeMismatch("top stack element must be dictionary to begin")

def end_dict_operation():
    check_dict_stack_underflow(1, "end")
    dict_stack.pop()

def length_operation():
    check_op_stack_underflow(1, "length")
    is_dict = isinstance(op_stack[-1], dict)
    is_dict_with_capacity = isinstance(op_stack[-1], DictWithCapacity)
    if is_dict or is_dict_with_capacity:
        op_stack.append(len(op_stack[-1]))
    elif is_mutable_string(op_stack[-1]):
        op_stack.append(len(op_stack[-1].string))
    else: 
        raise TypeMismatch("top stack element must be collection to length")

def maxlength_operation():
    check_op_stack_underflow(1, "maxlength")
    if  isinstance(op_stack[-1], DictWithCapacity): # only user defined dictationaries have capacity
        op_stack.append(op_stack[-1].capacity)
    else: 
        raise TypeMismatch("top stack element must be collection to maxlength")

# operations that may div by zero
div = lambda x, y: x / y
idiv = lambda x, y: x // y
mod = lambda x, y: x % y

def binary_operation(op: Callable):
    check_op_stack_underflow(2, op.__name__)
    if is_num(op_stack[-1]) and is_num(op_stack[-2]):
        op1 = op_stack.pop()
        if op1 == 0 and (op in [div, idiv, mod]):
            raise DivByZero("dividing by zero is invalid")
        op2 = op_stack.pop()
        res = op(op2, op1)
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation binary")
        
def unary_operation(op: Callable):
    check_op_stack_underflow(1, op.__name__)
    if is_num(op_stack[-1]):
        op_stack[-1] = op(op_stack[-1])
    elif is_bool(op_stack[-1]):
        op_stack[-1] = op(op_stack[-1])
    else:
        raise TypeMismatch("top stack element must be number to apply operation")

div_operation = lambda: binary_operation(div)
idiv_operation = lambda: binary_operation(idiv)
mod_operation = lambda: binary_operation(mod)
add_operation = lambda: binary_operation(lambda x, y: x + y)
mul_operation = lambda: binary_operation(lambda x, y: x * y)
sub_operation = lambda: binary_operation(lambda x, y: x - y)
abs_operation = lambda: unary_operation(abs)
neg_operation = lambda: unary_operation(lambda x: -x)
ceil_operation = lambda: unary_operation(math.ceil)
floor_operation = lambda: unary_operation(math.floor)
round_operation = lambda: unary_operation(round)
sqrt_operation = lambda: unary_operation(math.sqrt)
ne_operation = lambda: binary_operation(lambda x, y: x != y)
eq_operation = lambda: binary_operation(lambda x, y: x == y)
ge_operation = lambda: binary_operation(lambda x, y: x >= y)
gt_operation = lambda: binary_operation(lambda x, y: x > y)
le_operation = lambda: binary_operation(lambda x, y: x <= y)
lt_operation = lambda: binary_operation(lambda x, y: x < y)
and_operation = lambda: binary_operation(lambda x, y: x and y)
not_operation = lambda: unary_operation(lambda x: not x)
or_operation = lambda: binary_operation(lambda x, y: x or y)
true_operation = lambda: op_stack.append(True)
false_operation = lambda: op_stack.append(False)

def dup_operation():
    check_op_stack_underflow(1, "dup")
    op_stack.append(op_stack[-1])

def exch_operation():
    check_op_stack_underflow(2, "exch")
    op_stack.extend([op_stack.pop(), op_stack.pop()])

def pop_operation():
    """rm top stack element"""
    check_op_stack_underflow(1, "pop")
    op_stack.pop()

def clear_operation():
    op_stack.clear()

def pop_and_print():
    check_op_stack_underflow(1, "pop")
    print(op_stack.pop())

def double_equal_operation():
    check_op_stack_underflow(1, "==")
    op = op_stack.pop()
    if is_mutable_string(op):
        print(f"({op})")
    else:
        print(op)

def print_operation():
    check_op_stack_underflow(1, "print")
    if is_mutable_string(op_stack[-1]):
        print(f"{op_stack.pop()}")
        return
    
    raise TypeMismatch("top stack element must be string to print")

def count_operation():
    op_stack.append(len(op_stack))

def copy_operation():
    check_op_stack_underflow(1, "copy")
    n = op_stack[-1]
    check_op_stack_underflow(n, "copy")
    elements_to_copy = op_stack[:-1][::-1][:n+1][::-1]
    op_stack.pop()
    op_stack.extend(elements_to_copy)
    
def get_operation():
    check_op_stack_underflow(2, "get")
    if is_mutable_string(op_stack[-2]) and is_int(op_stack[-1]):
        index = op_stack.pop()
        string = op_stack.pop().string
        ascii = ord(string[index])
        op_stack.append(ascii)
    else:
        raise TypeMismatch("Wrong operands for operation get")

def getinterval_operation():
    check_op_stack_underflow(3, "getinterval")
    if is_mutable_string(op_stack[-3]) and is_int(op_stack[-2]) and is_int(op_stack[-1]):
        end, start, string = [op_stack.pop() for _ in range(3)]
        op_stack.append(string.string[start:end+1])
    else:
        raise TypeMismatch("Wrong operands for operation getinterval")

def put_interval_operation():
    """ string1 index string2 putinterval"""
    check_op_stack_underflow(3, "putinterval")
    if is_mutable_string(op_stack[-3]) and is_int(op_stack[-2]) and is_mutable_string(op_stack[-1]):
        string2, index, string1 = [op_stack.pop() for _ in range(3)] 
        string1.putinterval(index, string2.string) # Modify string1 in place
    else:
        raise TypeMismatch("Wrong operands for operation putinterval")
            
def if_operation():
    check_op_stack_underflow(2, "if")
    if is_list(op_stack[-1]) and is_bool(op_stack[-2]):
        process, boolean = op_stack.pop(), op_stack.pop()
        evaluate_list_of_inputs(process if boolean else [])
    else:
        raise TypeMismatch("Wrong operands for operation if")

def ifelse_operation():
    check_op_stack_underflow(3, "ifelse")
    if is_list(op_stack[-1]) and is_list(op_stack[-2]) and is_bool(op_stack[-3]):
        process_else, process_if, boolean = [op_stack.pop() for _ in range(3)]
        if boolean:
            evaluate_list_of_inputs(process_if)
        else:
            evaluate_list_of_inputs(process_else)
    else:
        raise TypeMismatch("Wrong operands for operation ifelse")

def for_operation():
    check_op_stack_underflow(4, "for")
    if is_list(op_stack[-1]) and is_int(op_stack[-2]) and is_int(op_stack[-3]) and is_int(op_stack[-4]):
        code_block, bound, increment, i = [op_stack.pop() for _ in range(4)]
        # run code block 
        for i in range(i, bound+1, increment):
            op_stack.append(i)
            evaluate_list_of_inputs(code_block)

    raise TypeMismatch("Wrong operands for operation for")

def repeat_operation():
    check_op_stack_underflow(2, "repeat")
    if is_list(op_stack[-1]) and is_int(op_stack[-2]):
        code_block, num_times = [op_stack.pop() for _ in range(2)]
        # execute the code block num times
        for _ in range(num_times):
            evaluate_list_of_inputs(code_block)
    
    raise TypeMismatch("Wrong operands for operation repeat")

def switch_to_lexical_scope():
    global scoping
    scoping = "LEXICAL"

def switch_to_dynamic_scope():
    global scoping
    scoping = "DYNAMIC"

def reset_dict_stack():

    # reset and add back in post script commands
    dict_stack.clear()
    dict_stack.append({})

    # add arithmetic operations to the global dictionary/scope
    dict_stack[-1]["add"] = add_operation
    dict_stack[-1]["mul"] = mul_operation
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

    # io operations
    dict_stack[-1]["="] = pop_and_print
    dict_stack[-1]["=="] = double_equal_operation
    dict_stack[-1]["print"] = print_operation

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

    # string operations
    dict_stack[-1]["length"] = length_operation
    dict_stack[-1]["get"] = get_operation
    dict_stack[-1]["getinterval"] = getinterval_operation
    dict_stack[-1]["putinterval"] = put_interval_operation

    # control flow operations
    dict_stack[-1]["if"] = if_operation
    dict_stack[-1]["ifelse"] = ifelse_operation
    dict_stack[-1]["for"] = for_operation
    dict_stack[-1]["repeat"] = repeat_operation

    # scope operations
    dict_stack[-1]["lexical"] = switch_to_lexical_scope
    dict_stack[-1]["dynamic"] = switch_to_dynamic_scope

reset_dict_stack()

def lookup_in_dictionary(input):

    if scoping == "DYNAMIC" or scoping == "LEXICAL":
        for scope in dict_stack[::-1]:
            if input in scope:
                value = scope[input]
                if callable(value): # checks if python func
                    value()
                elif isinstance(value, list):
                    evaluate_list_of_inputs(value)
                else:
                    op_stack.append(value)    
                return
         
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

def evaluate_list_of_inputs(input_list):
    """
    This function will process the contents of a code block.
    If using lexical scoping, it will search for the closure
    belonging to that code block and brielfy suspend the 
    dynamic scoping dict stack while the input is being evaluated.
    """

    # Suspend dynamic scoping if lexically scoped
    if scoping == "LEXICAL":
        closure = find_closure(input_list)
        if closure is not None:
            scope_when_defined = closure
            dict_stack.extend(scope_when_defined)

    # eval each command
    for input in input_list:
        process_input(input)

    # Resume dynamic scoping if lexically scoped
    if scoping == "LEXICAL":
        for _ in range(len(scope_when_defined)):
            dict_stack.pop()

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

def find_closure(code_block):
    for closure in closures:
        if closure.code_block == code_block:
            return closure.dict_stack

def process_constants(input):
    for parser in PARSERS:
        try:
            res = parser(input)

            # when encountering a code block, create closure of the state of the dict stack
            if isinstance(res, list):
                new_closure = Closure(res, dict_stack.copy())
                closures.append(new_closure)  
                              
            op_stack.append(res)
            return 
        except ParseFailed as e:
            logging.debug(e)
            continue
    raise ParseFailed(f"None of the parsers worked for the input {input}")


if __name__ == "__main__":
    repl()