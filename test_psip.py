import psip
from exceptions import DivByZero, StackUnderflow
import random
import math
from dict_with_capacity import DictWithCapacity

def two_random_numbers():
	two_nums = (random.randint(0, 100), random.randint(0, 100))
	two_nums_str = (str(two_nums[0]), str(two_nums[1]))
	return two_nums, two_nums_str

def test_add_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1]) 
	psip.process_input("add")
	assert psip.op_stack[-1] == two_nums[0] + two_nums[1]

def test_lookup_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input("/x")
	psip.process_input(two_nums_str[1])
	psip.process_input("x")
	assert psip.op_stack[-1] == two_nums[1]

def test_sub_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("sub")
	assert psip.op_stack[-1] == two_nums[0] - two_nums[1]

def test_div_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	try:
		psip.process_input("div")
		assert psip.op_stack[-1] == two_nums[0] / two_nums[1]
	except DivByZero:
		pass 

def test_idiv_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	try:
		psip.process_input("idiv")
		assert psip.op_stack[-1] == two_nums[0] // two_nums[1]
	except DivByZero:
		pass 

def test_mod_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	try:
		psip.process_input("mod")
		assert psip.op_stack[-1] == two_nums[0] % two_nums[1]
	except DivByZero:
		pass 

def test_abs_operation():
	num = random.randint(-100, -1)
	psip.op_stack.clear()
	psip.process_input(str(num))
	psip.process_input("abs")
	assert psip.op_stack[-1] == abs(num)

def test_neg_operation():
	num = random.randint(-100, 100)
	psip.op_stack.clear()
	psip.process_input(str(num))
	psip.process_input("neg")
	assert psip.op_stack[-1] == -num

def test_sqrt_operation():
	num = random.randint(0, 100)
	psip.op_stack.clear()
	psip.process_input(str(num))
	psip.process_input("sqrt")
	assert psip.op_stack[-1] == math.sqrt(num)

def test_ceil_operation():
	num = random.randint(0, 100)
	psip.op_stack.clear()
	psip.process_input(str(num))
	psip.process_input("ceil")
	assert psip.op_stack[-1] == math.ceil(num)

def test_floor_operation():
	num = random.randint(0, 100)
	psip.op_stack.clear()
	psip.process_input(str(num))
	psip.process_input("floor")
	assert psip.op_stack[-1] == math.floor(num)
	
def test_round_operation():
	num = random.randint(0, 100)
	psip.op_stack.clear()
	psip.process_input(str(num))
	psip.process_input("round")
	assert psip.op_stack[-1] == round(num)

def test_dup_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input("dup")
	assert psip.op_stack[-1] == psip.op_stack[-2] == two_nums[0]

def test_exch_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("exch")
	assert psip.op_stack[-1] == two_nums[0]
	assert psip.op_stack[-2] == two_nums[1]

def test_pop_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input("pop")
	assert len(psip.op_stack) == 0
	
def test_clear_operation():
	two_nums, two_nums_str = two_random_numbers()
	psip.op_stack.clear()
	psip.process_input(two_nums_str[0])
	psip.process_input(two_nums_str[1])
	psip.process_input("clear")
	assert len(psip.op_stack) == 0

def test_count_operation():
	psip.op_stack.clear()    
	psip.process_input("count")
	assert psip.op_stack[-1] == 0
	psip.process_input("count")
	assert psip.op_stack[-1] == 1
	psip.process_input("count")
	assert psip.op_stack[-1] == 2

def test_copy_operation():
	psip.op_stack.clear()
	psip.process_input("1")
	psip.process_input("2")
	psip.process_input("3")
	psip.process_input("3")
	psip.process_input("copy")
	assert psip.op_stack == [1, 2, 3, 1, 2, 3]

def test_dynamic_scoping():
	psip.op_stack.clear()
	input = [
		r"/x", "1", "def",     # defined in global
		"1", "dict", "begin",  # start new dict
		r"/x", "2", "def",     # redef x in this scope
		"1", "dict", "begin",  # new scope
		"x",                   # put x onto the stack
	]
	for i in input:
		psip.process_input(i)
	psip.lookup_in_dictionary("x", dynamic_scoping=True)
	assert psip.op_stack[-1] == 2

def test_dict_with_capacity():
	d = DictWithCapacity(1)
	d["x"] = 1
	try:
		d["y"] = 2
		assert False
	except Exception as e:
		assert str(e) == "dict is full"

def test_dictionary_capacity():
	psip.op_stack.clear()
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

def test_dictionary_length():
	psip.op_stack.clear()
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