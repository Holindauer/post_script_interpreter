import psip
from exceptions import DivByZero, StackUnderflow
import random

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