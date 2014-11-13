#Initialize memory, registers, timers

#Must include sections so you don't have to code an offset
#Bytes are in hex, memory is a list of bytes (8-bits) so it is much more helpful to be in hex.
memory = [0x00 for x in range(0x1000)]

def clear_memory():
	memory = [0x00 for x in range(0x1000)]


#Registers
registers = [0x00 for x in range(0x10)]




#Display - 64 X 32
#List comprehension of a list comprehension -- a 64 item array of 32 item arrays.
display = [[True for x in range(32)] for x in range(64)]


#Returns empty display - takes up less memory looping through than having two lists at once.
def clear_display():
	for array in display:
		for item in array:
			item = True;
	


#Input - Hexidecimal keyboard created using list comprehension
#Boolean because we only need to know if key has been pressed or not. Using hex value because the keyboard is oringinally a hex one. 
keys = [False for x in range(0x10)]



#Timers - count down until 0
delay_timer = 0

#Sound is played only when this is at 0
sound_timer = 0



#Option to select rom
def load_rom(filepath):
	clear_display()
	with open(filepath, 'rb') as rom:
		data = rom.read()

	for byte in data:
		memory.append(byte)




#Load rom

#Display loop (infinite)

	#Eventually - limit to 60 fps


#Main 

