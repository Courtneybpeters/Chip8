#Initialization
finished = False

#Must include sections so you don't have to code an offset
#Bytes are in hex, memory is a list of bytes (8-bits) so hex is more helpful.
memory = [0x00 for x in range(0x1000)]


#Clears memory
def clear_memory():
	for byte in memory:
		byte = 0x00


#Registers
registers = [0x00 for x in range(0x10)]

#Program counter so execution can jump to different points in memory.
#Starts at where programs start within the memory.
I = 0x200

#Stack - pretty much a bookmark for addresses with jumps of execution. Think LIFO
stack = []


#Display - 64 X 32
#List comprehension of a list comprehension -- a 64 item array of 32 item arrays.
display = [[True for x in range(32)] for x in range(64)]




#Input - Hexidecimal keyboard created using list comprehension
#Boolean because we only need to know if key has been pressed or not. Using hex
#value because the keyboard is oringinally a hex one.
keys = [False for x in range(0x10)]

#Timers - count down until 0
delay_timer = 0

#Sound is played only when this is at 0
sound_timer = 0

#Opcode variable needs to be global
op_code = ''

#Option to select rom
def load_rom(filepath):
	clear_display()
	global I
	with open(filepath, 'rb') as rom:
		data = rom.read()

	#For each value in data, add it in the memory list. Add 1 so it starts from the program section of the memory.
	#QUESTION - First 0-512(0x200) is for the interpreter, correct?
	for byte in data:
		memory[I] = ord(byte)
		I += 1


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


# ----------------- Opcodes -----------------------------------

#00E0
#Returns empty display - takes up less memory looping through than having
#two lists at once.
def clear_display():
	for array in display:
		for item in array:
			item = True


#00EE - Returns from subroutine (aka a jump in execution.)
def return_address():
	I = stack.pop(-1)


#1NNN - Jumps to a certain address
def address_jump(address):
	I = address


#2NNN - Calls subroutine at that address
def subroutine(address):
	stack.append(I)
	I = address

#3XNN - Skip if equal to NN
def skip_if_equal(register, value):
	if registers[register] == value:
		#Add two because each opcode is two bytes (2 hex values)
		I += 2




#----------------------------------------------------------------

finished = False

#Main - read and parse opcodes out of memory.
def step():
	global I
	global finished
	I += 2

	if I == 0x1000:
		finished = True
		return

	first_byte = hex(memory[I])
	second_byte = hex(memory[I+1])
	#Opcode is a string
	op_code = first_byte[2:].zfill(2).upper() + second_byte[2:].zfill(2).upper()

	if op_code == "0000":
		finished = True
		return

	#These are integers
	nnn = int(op_code[1:], 16)
	nn = int(op_code[2:], 16)
	n = int(op_code[3], 16)
	x = int(op_code[1], 16)
	y = int(op_code[2], 16)

	#Handles '0' opcodes
	# if op_code[0] == "0":
	# 	if op_code == "00E0":
	# 		clear_display()
	# 	if op_code == "00EE":
	# 		return_address()
	#
	# if op_code[0] == "1":
	# 	address_jump(nnn)
	#
	# if op_code[0] == "2":
	# 	subroutine(nnn)
	#
	# if op_code[0] == "3":
		#Register will be x (register, ) and nn will be value


	print op_code



#Display loop (infinite) - use pygame

	#Eventually - limit to 60 fps


#Main - TKinter to load rom
if __name__ == "__main__":
	rom_path = raw_input("Enter the path of your rom: ")
	load_rom(rom_path)
	hex_dump("hexdump.txt", memory)
	while not finished:
		step()
	# print "Opcode: ", op_code
	# print "Opcode type: ", type(op_code)
