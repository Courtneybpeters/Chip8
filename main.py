#Initialize memory, registers, timers
memory = ['' for x in range(4096)]

#Display - 64 X 32
#List comprehension of a list comprehension -- an 64 item array of 32 item arrays.
display = [[True for x in range(32)] for x in range(64)]




#Input - Hexidecimal keyboard created using list comprehension
#QUESTION - Should I convert the integers to strings? Mixed type list seems like a bad idea.
keys = ['a', 'b', 'c', 'd', 'e', 'f'] + [digit for digit in range(10)]



#Timers - count down until 0
delay_timer = 60

#Sound is played only when this is at 0
sound_timer = 60



#Option to select rom

#Load rom

#Display loop (infinite)

	#Eventually - limit to 60 fps