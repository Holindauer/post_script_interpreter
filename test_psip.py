import psip
from exceptions import DivByZero, StackUnderflow
import random
import math
from utils import DictWithCapacity
import pytest # type: ignore

@pytest.fixture
def reset_psip():
	psip.op_stack.clear()
	psip.reset_dict_stack()
	psip.closures.clear()
	psip.scoping = "DYNAMIC"

def two_random_numbers():
	two_nums = (random.randint(0, 100), random.randint(0, 100))
	two_nums_str = (str(two_nums[0]), str(two_nums[1]))
	return two_nums, two_nums_str

def test_add_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1]) 
	psip.process_input("add")
	assert psip.op_stack[-1] == two_nums[0] + two_nums[1]

def test_lookup_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input("/x")
	psip.process_input(two_nums_str[1])
	psip.process_input("x")
	assert psip.op_stack[-1] == two_nums[1]

def test_sub_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("sub")
	assert psip.op_stack[-1] == two_nums[0] - two_nums[1]

def test_ne_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("ne")
	assert psip.op_stack[-1] == (two_nums[0] != two_nums[1])

def test_eq_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("eq")
	assert psip.op_stack[-1] == (two_nums[0] == two_nums[1])

def test_ge_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("ge")
	assert psip.op_stack[-1] == (two_nums[0] >= two_nums[1])

def test_gt_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("gt")
	assert psip.op_stack[-1] == (two_nums[0] > two_nums[1])

def test_le_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("le")
	assert psip.op_stack[-1] == (two_nums[0] <= two_nums[1])

def test_lt_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("lt")
	assert psip.op_stack[-1] == (two_nums[0] < two_nums[1])

def test_or_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("or")
	assert psip.op_stack[-1] == (two_nums[0] or two_nums[1])

def test_div_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	try:
		psip.process_input("div")
		assert psip.op_stack[-1] == two_nums[0] / two_nums[1]
	except DivByZero:
		pass 

def test_idiv_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	try:
		psip.process_input("idiv")
		assert psip.op_stack[-1] == two_nums[0] // two_nums[1]
	except DivByZero:
		pass 

def test_mod_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	try:
		psip.process_input("mod")
		assert psip.op_stack[-1] == two_nums[0] % two_nums[1]
	except DivByZero:
		pass 
	
def test_mul_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("mul")
	assert psip.op_stack[-1] == two_nums[0] * two_nums[1]

def test_abs_operation(reset_psip):
	num = random.randint(-100, -1)
	psip.process_input(str(num))
	psip.process_input("abs")
	assert psip.op_stack[-1] == abs(num)

def test_false(reset_psip):
	psip.process_input("false")
	assert psip.op_stack[-1] == False

def test_true(reset_psip):
	psip.process_input("true")
	assert psip.op_stack[-1] == True

def test_not_operation(reset_psip):
	psip.process_input("true")
	psip.process_input("not")
	assert psip.op_stack[-1] == (not True)

def test_neg_operation(reset_psip):
	num = random.randint(-100, 100)
	psip.process_input(str(num))
	psip.process_input("neg")
	assert psip.op_stack[-1] == -num

def test_sqrt_operation(reset_psip):
	num = random.randint(0, 100)
	psip.process_input(str(num))
	psip.process_input("sqrt")
	assert psip.op_stack[-1] == math.sqrt(num)

def test_ceil_operation(reset_psip):
	num = random.randint(0, 100)
	psip.process_input(str(num))
	psip.process_input("ceil")
	assert psip.op_stack[-1] == math.ceil(num)

def test_floor_operation(reset_psip):
	num = random.randint(0, 100)
	psip.process_input(str(num))
	psip.process_input("floor")
	assert psip.op_stack[-1] == math.floor(num)
	
def test_round_operation(reset_psip):
	num = random.randint(0, 100)
	psip.process_input(str(num))
	psip.process_input("round")
	assert psip.op_stack[-1] == round(num)

def test_dup_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input("dup")
	assert psip.op_stack[-1] == psip.op_stack[-2] == two_nums[0]

def test_exch_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("exch")
	assert psip.op_stack[-1] == two_nums[0]
	assert psip.op_stack[-2] == two_nums[1]

def test_pop_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input("pop")
	assert len(psip.op_stack) == 0
	
def test_clear_operation(reset_psip):
	two_nums, two_nums_str = two_random_numbers()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("clear")
	assert len(psip.op_stack) == 0

def test_count_operation(reset_psip):
	psip.process_input("count")
	assert psip.op_stack[-1] == 0
	psip.process_input("count")
	assert psip.op_stack[-1] == 1
	psip.process_input("count")
	assert psip.op_stack[-1] == 2

def test_copy_operation(reset_psip):
	psip.process_input("1")
	psip.process_input("2")
	psip.process_input("3")
	psip.process_input("3")
	psip.process_input("copy")
	assert psip.op_stack == [1, 2, 3, 1, 2, 3]

def test_dict_with_capacity():
	d = DictWithCapacity(1)
	d["x"] = 1
	try:
		d["y"] = 2
		assert False
	except Exception as e:
		assert str(e) == "dict is full"

def test_dictionary_capacity(reset_psip):
	psip.process_input("1")
	psip.process_input("dict")
	psip.process_input("begin")
	psip.process_input("/x")
	psip.process_input("1")
	psip.process_input("def")
	psip.process_input("/x2")
	psip.process_input("1")
	psip.process_input("def")
	assert len(psip.dict_stack[-1]) == 1
	psip.process_input("end")

def test_dictionary_length(reset_psip):
	input = [
		r"/d", "10", "dict", "def",
		"d", "begin",
		r"/x", "1", "def",
		r"/y", "3", "def",
		"d", "length"
	]
	for command in input:
		psip.process_input(command)

	print(psip.op_stack[-1])
	assert psip.op_stack[-1] == 2

	psip.process_input("end")


def test_dictionary_maxlength(reset_psip):
	input = [
		r"/d", "10", "dict", "def",
		"d", "maxlength"
	]
	for command in input:
		psip.process_input(command)

	print(psip.op_stack[-1])
	assert psip.op_stack[-1] == 10

def test_string(reset_psip):
	psip.process_input("(hello)")
	assert psip.op_stack[-1].string == "hello"

def test_string_length(reset_psip):
	string = "hello"
	psip.process_input(f"({string})")
	psip.process_input("length")
	assert psip.op_stack[-1] == len(string)

def test_get_operation(reset_psip):
	psip.process_input("(hello)")
	psip.process_input("1")
	psip.process_input("get")
	assert psip.op_stack[-1] == ord("e")

def test_getinterval_operation(reset_psip):
	psip.process_input("(hello)")
	psip.process_input("1")
	psip.process_input("3")
	psip.process_input("getinterval")
	assert psip.op_stack[-1] == "ell"

def test_putinterval_operation(reset_psip):
	psip.process_input("(hello)")
	psip.process_input("dup")
	psip.process_input("1")
	psip.process_input("(hi)")
	psip.process_input("putinterval")
	assert psip.op_stack[-1].string == "hhilo"

def test_if_operation_true(reset_psip):
	input = "true", "{1 2 add}", "if"
	for command in input:
		psip.process_input(command)
	assert psip.op_stack[-1] == 3

def test_if_operation_false(reset_psip):
	input = "false", "{1 2 add}", "if"
	for command in input:
		psip.process_input(command)
	assert len(psip.op_stack) == 0

def test_ifelse_operation_true(reset_psip):
	input = "true", "{1 2 add}", "{2 2 add}", "ifelse"
	for command in input:
		psip.process_input(command)
	assert psip.op_stack[-1] == 3

def test_ifelse_operation_false(reset_psip):
	input = "false", "{1 2 add}", "{2 2 add}", "ifelse"
	for command in input:
		psip.process_input(command)
	assert psip.op_stack[-1] == 4

def test_for_operation(reset_psip):
	input = psip.lexer("0 0 1 10 {add} for")
	for command in input:
		psip.process_input(command)
	assert psip.op_stack[-1] == 55

def test_repeat_operation():
	psip.op_stack.clear()
	input = psip.lexer("10 { 10 } repeat")
	for command in input:
		psip.process_input(command)
	for i in range(10):
		assert psip.op_stack[-1 - i] == 10

def test_dynamic_scoping(reset_psip):
	input = [
		r"/x", "1", "def",     # defined in global
		"1", "dict", "begin",  # start new dict
		r"/x", "2", "def",     # redef x in this scope
		"1", "dict", "begin",  # new scope
		"x",                   # put x onto the stack
	]
	for i in input:
		psip.process_input(i)
	psip.lookup_in_dictionary("x")
	assert psip.op_stack[-1] == 2


def test_closure(reset_psip):
	input = psip.lexer(r"/x { 1 } def ")
	for command in input:
		psip.process_input(command)

	# this should grab the state of the dict stack at the time
	# the closure was created. In this particular case, it should
	# be equal but not the same object.
	global_dict_stack = psip.dict_stack
	code_block = global_dict_stack[-1]["x"]
	closure_dict_stack = psip.find_closure(code_block)

	assert global_dict_stack is not closure_dict_stack

	# the dict stack at the time of definition should not contain the value of x
	assert global_dict_stack[-1]["x"] == ['1']
	if "x" in closure_dict_stack[-1]:
		assert False
	
def test_closure_with_function(reset_psip):
	input = psip.lexer(
		r"""
		/x  1  def  
		/y { x } def 
		/x 2 def 
		"""
		)
	for command in input:
		psip.process_input(command)

	global_dict_stack = psip.dict_stack

	code_block = global_dict_stack[-1]["y"]
	closure_dict_stack = psip.find_closure(code_block)

	# the closure dict stack should contain the state 
	# of x at the time of defining the y function.
	assert global_dict_stack is not closure_dict_stack
	assert global_dict_stack[-1]["x"] == 2
	assert closure_dict_stack[-1]["x"] == 1
	
def lexical_scoping_test_helper(code_string, expected_top_stack_element):
	input = psip.lexer(code_string)
	for command in input:
		psip.process_input(command)
	assert psip.scoping == "LEXICAL"
	assert psip.op_stack[-1] == expected_top_stack_element

def test_lexical_scoping(reset_psip):
	# func returns x, and x was 1 at time of definition,
	# so func should return 1.
	lexical_scoping_test_helper(
		"""
		lexical
		/x 1 def 
		/func { x } def 
		/x 2 def 
		func
		""",
		expected_top_stack_element = 1
	)
def test_lexical_scoping_2(reset_psip):
	# y is called, which calls f. Within the scope of f, x 
	# is defined as 1, and x is returned, so y should return 1.
	lexical_scoping_test_helper(
		"""
		lexical
		/x 9 def
		/f { /x 1 def x } def
		/y { /x 2 def f } def 
		/x 8 def
		y
		""",
		expected_top_stack_element = 1
	)

def test_lexical_scoping_3(reset_psip):
	# y defineds a function that calls f at the end. When y
	# was defined, x was equal to 9, so y should return 9.
	lexical_scoping_test_helper(
		"""
		lexical
		/x 9 def
		/f { x } def
		/y { /x 2 def f } def 
		/x 8 def
		y
		""",
		expected_top_stack_element = 9
	)

def test_lexical_scoping_4(reset_psip):
	# x is defined as 8, when x is called it should return 8.
	# the prior definitions should not affect this.
	lexical_scoping_test_helper(
		"""
		lexical
		/x 9 def
		/f { x } def
		/y { /x 2 def f } def 
		/x 8 def
		x
		""",
		expected_top_stack_element = 8
	)