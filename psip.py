import logging
from exceptions import ParseFailed, TypeMismatch
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
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op1 + op2 
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation add")
    
def sub_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op2 - op1  # rev bc postfix, so { 1 2 sub } == -1
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation add")

def div_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if op1 == 0:
            raise DivByZero("dividing by zero is invalid")
        res = op2 / op1  # rev bc postfix, so { 1 2 div } == 1 / 2
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation div")

def mod_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if op1 == 0:
            raise DivByZero("dividing by zero is invalid")
        res = op2 % op1  # rev bc postfix, so { 1 2 mod } == 1 % 2 
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation mod")

# add operations to the global dictionary/scope
dict_stack[-1]["add"] = add_operation
dict_stack[-1]["def"] = def_operation
dict_stack[-1]["sub"] = sub_operation
dict_stack[-1]["div"] = div_operation
dict_stack[-1]["mod"] = mod_operation

def pop_and_print():
    if(len(op_stack) >= 1):
        op1 = op_stack.pop()
        print(op1)
    else:
        raise TypeMismatch("Stack is empty! nothin to print")
    
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