import random


#Address QUESTIONs and TODO (Ctrl+ Shift + T)

#--------------------- Initialization --------------------------------------

finished = False
memory = []
registers = []
I = 0x0000
PC = 0x00
delay_timer = 0
sound_timer = 0
stack = []
display = []
keys = []
op_code = ''
sprite_lookup = []


#---------------------------- Reset Function-----------------------------------

def reset():
	global finished
	finished = False

	#Must include sections so you don't have to code an offset
	#Bytes are in hex, memory is a list of bytes (8-bits) so hex is more helpful.
	global memory
	# memory = [0x00 for x in range(0x1000)]
	memory = [0xF0, 0x90, 0x90, 0x90, 0xF0,
	 0x20, 0x60, 0x20, 0x20, 0x70,
	 0xF0, 0x10, 0xF0, 0x80, 0xF0,
	 0xF0, 0x10, 0xF0, 0x10, 0xF0,
	 0x90, 0x90, 0xF0, 0x10, 0x10,
	 0xF0, 0x80, 0xF0, 0x10, 0xF0,
	 0xF0, 0x80, 0xF0, 0x90, 0xF0,
	 0xF0, 0x10, 0x20, 0x40, 0x40,
	 0xF0, 0x90, 0xF0, 0x90, 0xF0,
	 0xF0, 0x90, 0xF0, 0x10, 0xF0,
	 0xF0, 0x90, 0xF0, 0x90, 0x90,
	 0xE0, 0x90, 0xE0, 0x90, 0xE0,
	 0xF0, 0x80, 0x80, 0x80, 0xF0,
	 0xE0, 0x90, 0x90, 0x90, 0xE0,
	 0xF0, 0x80, 0xF0, 0x80, 0xF0,
	 0xF0, 0x80, 0xF0, 0x80, 0x80
	 ]

	memory.extend([0x00] * 0xFB0)

	#Registers
	#QUESTION - can this hex value be written as 0x0 because it will never go above 15 aka F?
	#or is it because its 8-bits (aka two hex values?)
	global registers
	registers = [0x00 for x in range(0x10)]

	#Register I - used for drawing
	global I
	I = 0x0000

	#Program counter so execution can jump to different points in memory.
	#Starts at where programs start within the memory.
	global PC
	PC = 0x200

	#Timers - count down until 0
	global delay_timer
	delay_timer = 0

	#Sound is played only when this is at 0
	global sound_timer
	sound_timer = 0

	#Stack - pretty much a bookmark for addresses with jumps of execution. Think LIFO
	global stack
	stack = []


	#Display - 64 X 32
	#List comprehension of a list comprehension -- a 64 item array of 32 item arrays.
	global display
	display = [[True for x in range(64)] for x in range(32)]


	#Input - Hexidecimal keyboard created using list comprehension
	#Boolean because we only need to know if key has been pressed or not. Using hex
	#value because the keyboard is oringinally a hex one.
	global keys
	keys = [False for x in range(0x10)]

	#Opcode variable needs to be global
	global op_code
	op_code = ''



#-------------------------- Loading Rom --------------------------------

#Option to select rom
def load_rom(filepath):
	clear_display()
	address = PC
	with open(filepath, 'rb') as rom:
		data = rom.read()

	#For each value in data, add it in the memory list. Add 1 so it starts from the program section of the memory.
	for byte in data:
		memory[address] = ord(byte)
		address += 1


def hex_dump(file, memory):
	line_wrap = 0
	with open(file, 'w') as hex_dump:
		for value in memory:
			if line_wrap % 16 == 0:
				hex_dump.write(hex(line_wrap)[2:].upper().zfill(3) + ': ')
			hex_dump.write(hex(value)[2:].upper().zfill(2) + ' ')
			line_wrap += 1
			if line_wrap % 16 == 0:
				hex_dump.write('\n')


# --------------------------- Opcodes ----------------------------------------

#00E0 - Returns empty display -
#takes up less memory looping through than having two lists at once.
def clear_display():
	for array in display:
		for item in array:
			item = True

#00EE - Returns from subroutine (aka a jump in execution.)
def return_address():
	global PC
	global stack
	PC = stack.pop(-1)

#1NNN - Jumps to a certain address
def address_jump(address):
	global PC
	PC = address

#2NNN - Calls subroutine at that address
def subroutine(address):
	global PC
	global stack
	stack.append(PC)
	PC = address

#3XNN - Skip if equal to NN
def skip_if_equal(register, value):
	global PC
	if registers[register] == value:

		#Add 2 because each opcode is two bytes (2 hex values) and we already
		#added two within the step function to get to the rest of the opcode
		PC += 2

#4XNN - Skip if not equal to NN
def skip_if_unequal(register, value):
	global PC
	if registers[register] != value:
		PC += 2

#5XY0 - Skips instruction if two registers are equal
def register_equal_skip(a, b):
	global PC
	if registers[a] == registers[b]:
		PC += 2

#6XNN - Sets register to a value
def set_register(register, value):
	registers[register] = value

#7XNN - Adds to a register
def register_add_value(register, value):
	registers[register] += value

#8XY0 - Sets register to the value of the other register
def register_a_b_set(a, b):
	registers[a] = registers[b]

#8XY1 - Bitwise OR two registers
def or_register(a, b):
	registers[a] |= registers[b]

#8XY2 - Bitwise AND two registers
def and_register(a, b):
	registers[a] &= registers[b]

#8XY3 - Bitwise XOR two registers
def xor_register(a, b):
	registers[a] ^= registers[b]

#8XY4 - Add register b to a, register f == 1 if there is a carry, else 0
def add_two_registers(a, b):
	if registers[a] + registers[b] > 255:
		registers[0xF] = 0x01
		registers[a] += registers[b] - 256

	else:
		registers[0xF] = 0x00
		registers[a] += registers[b]


#8XY5 - Subtracts x from y, register f = 1
def registers_subtract(a, b):
    #F indicates NOT borrowed, so if we didn't borrow, set it to true(1)
	if registers[a] > registers[b]:
		registers[0xF] = 0x01

	else:
		registers[0xF] = 0x00

	registers[a] = abs(registers[a] - registers[b])


#8XY6 - Shift register to the right by one
def shift_right(register):
	registers[0xF] = registers[register] % 2

	registers[register] >>= 1

#8XYE - Shifts register left
def shift_left(register):
	if registers[register] > 127:
		registers[0xF] = 0x01

	else:
		registers[0xF] = 0x00

	registers[register] <<= 1
	registers[register] %= 256


#9XY0 - Skip instruction if a doesn't equal b
def register_unequal_skip(a, b):
	global PC
	if registers[a] != registers[b]:
		PC += 2

#ANNN - Sets I to a certain address
def set_I(address):
	global I
	I = address

#BNNN - Jumps to address of nnn + the first register
def jump_first_reg(value):
	global PC
	PC = value + registers[0x0]

#CXNN - Set register to a value AND random number
def set_random(register, value):
	rand_number = random.randrange(256)
	registers[register] = value & rand_number

#TODO DXYN - Draws to the screen
def draw(a, b, n):
	global I
	y = registers[b] % 32
	registers[0xF] = 0x00
	for byte in range(n):
		x = registers[a] % 64
		line = memory[I + byte]
		line = bin(line)[2:].zfill(8)
		for index in range(len(line)):
			bit = int(line[index])
			pixel = display[y][x]
			if pixel == True and bit == 1:
				registers[0xF] = 0x01

			display[y][x] = pixel ^ bit
			x += 1
			if x > 63:
				x = 0
		y += 1
		if y > 31:
			y = 0


#TODO EX9E/EXA1 - We test whether or not a key was pressed in the register passed
def key_press(register):
	global PC
	#Run input function and check what gets stored?
	return


#FX07 - Set register to value of timer
def set_reg_to_delay(register):
	registers[register] = delay_timer

#FX0A - Stores key pressed in a register (raw_input pretty much)
#TODO - Keys via keyboard or on screen keys?
def input_to_register(register):
	registers[register] = int(raw_input())

#FX15 - Sets delay timer to the value of register x
def set_delay_timer(register):
	global delay_timer
	delay_timer = registers[register]

#FX18 - Sets sound timer to value of register x
def set_sound_timer(register):
	global sound_timer
	sound_timer = registers[register]

#FX1E - Adds register and value of I and sets result as I
def add_to_stack(register):
	global I
	I += registers[register]

#FX29 - location of sprite
def sprite(register):
	global I
	I = registers[register] * 5

#FX33 - Binary coded decimal representation
def bcd(register):
	x = registers[register]
	memory[I] = x / 100
	x %= 100
	memory[I + 1] = x / 10
	memory[I + 2] = x % 10

#FX55 - Stores group of registers in memory
def store_reg_in_mem(end):
	location = I
	for register in range(end + 1):
		memory[location] = registers[register]
		location += 1

#FX65 - Reads group of registers from memory
def read_from_memory(end):
	location = I
	count = 0
	for data in range(location, end + 1):
		registers[count] = memory[data]
		count += 1
		location += 1





#------------------------ Opcode Logic -------------------------

#Step parses out opcodes and calls the appropriate function.
def step():
	global PC
	global finished

	# Debugging
	# print "PC = ", PC

	#QUESTION -- doing this so then i don't have the issue of trying to parse a
	#opcode outside range of memory.
	if PC == 0x1000:
		finished = True
		return

	first_byte = hex(memory[PC])
	second_byte = hex(memory[PC+1])
	#Opcode is a string
	op_code = first_byte[2:].zfill(2).upper() + second_byte[2:].zfill(2).upper()

	#Values within opcodes
	nnn = int(op_code[1:], 16)
	nn = int(op_code[2:], 16)
	n = int(op_code[3], 16)
	x = int(op_code[1], 16)
	y = int(op_code[2], 16)

	print op_code

	#Increment Program Counter (PC)
	PC += 2


	#Directing to correct opcodes

	#Multiple 0 opcodes
	if op_code[0] == "0":
		if op_code == "00E0":
			clear_display()
		if op_code == "00EE":
			return_address()
	#
	if op_code[0] == "1":
		address_jump(nnn)

	elif op_code[0] == "2":
		subroutine(nnn)

	elif op_code[0] == "3":
		skip_if_equal(x, nn)

	elif op_code[0] == "4":
		skip_if_unequal(x, nn)

	elif op_code[0] == "5":
		register_equal_skip(x, y)

	elif op_code[0] == "6":
		set_register(x, nn)

	elif op_code[0] == "7":
		register_add_value(x, nn)

	#Multiple 8 opcodes
	elif op_code[0] == "8":
		if op_code[3] == "0":
			register_a_b_set(x, y)

		if op_code[3] == "1":
			or_register(x, y)

		if op_code[3] == "2":
			and_register(x, y)

		if op_code[3] == "3":
			xor_register(x, y)

		if op_code[3] == "4":
			add_two_registers(x, y)

		if op_code[3] == "5":
			registers_subtract(x, y)


		if op_code[3] == "6":
			shift_right(x)

		if op_code[3] == "7":
			registers_subtract(y, x)

		if op_code[3] == "E":
			shift_left(x)

	elif op_code[0] == "9":
		register_unequal_skip(x, y)

	elif op_code[0] == "A":
		set_I(nnn)

	elif op_code[0] == "B":
		jump_first_reg(nnn)

	elif op_code[0] == "C":
		set_random(x, nn)

	elif op_code[0] == "D":
		draw(x, y, n)

	elif op_code[0] == "E":
		key_press(x)

	#Multiple F opcodes
	elif op_code[0] == "F":
		if op_code[3] == "7":
			set_reg_to_delay(x)

		elif op_code[3] == "A":
			input_to_register(x)

		elif op_code[2:3] == "15":
			set_delay_timer(x)

		elif op_code[3] == "8":
			set_sound_timer(x)

		elif op_code[3] == "E":
			add_to_stack(x)

		elif op_code[3] == "9":
			sprite(x)

		elif op_code[3] == "3":
			bcd(x)

		elif op_code[2:3] == "55":
			store_reg_in_mem(x)

		elif op_code[2:3] == "65":
			read_from_memory(x)


#Display loop (infinite) - use pygame

	#Eventually - limit to 60 fps


#Main - TKinter to load rom
if __name__ == "__main__":
	rom_path = raw_input("Enter the path of your rom: ")
	load_rom(rom_path)
	hex_dump("hexdump.txt", memory)
	count = 0
	while not finished:
		step()
		count += 1
		if count == 10:
			break
	# print "Opcode: ", op_code
	# print "Opcode type: ", type(op_code)
