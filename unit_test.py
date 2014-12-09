import unittest
import main

#TODO - QUESTION - Can I just assign two of the registers a value in the setup
#                  so I don't have to keep checking they're zero, setting them,
#                  and then performing a function on them?

#       QUESTION - Why am I having to make PC and I global in all my functions but not
#                  the registers array?

class Test_Chip_8(unittest.TestCase):
    def setUp(self):
        main.reset()

    def test_jump(self):
        print
        print "Testing address_jump function"

        #Calls the function --> Function's side effects changes a value.
        main.address_jump(0x400)

        #Now assert to ensure the value is correct after it's been changed
        #from the line above.
        self.assertEqual(main.PC, 0x400)
        print "address_jump passed."

    def test_jump_and_return(self):
        print
        print "Testing jump to subroutine function"
        main.subroutine(0x400)
        self.assertEqual(main.stack[0], 0x200)
        self.assertEqual(main.PC, 0x400)
        print "jump to subroutine passed."
        print
        print "Testing return from subroutine function"
        main.return_address()
        self.assertEqual(len(main.stack), 0)
        self.assertEqual(main.PC, 0x200)
        print "return from subroutine passed."


    def test_register_value(self):
        print
        print "Testing register assignment function"
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x40)
        self.assertEqual(main.registers[5], 0x40)
        print "register assignment passed."
        print

        print "Testing skip if equal function - equal"
        main.skip_if_equal(5, 0x40)
        self.assertEqual(main.PC, 0x202)
        print "Skip if equal - equal passed."
        print
        print "Testing skip if equal function - unequal"
        main.skip_if_equal(5, 0x50)
        self.assertEqual(main.PC, 0x202)
        print "Skip if equal - unequal passed."
        print
        print "Testing skip if unequal function - unequal"
        main.skip_if_unequal(5, 0x50)
        self.assertEqual(main.PC, 0x204)
        print "Skip if unequal - unequal passed."
        print
        print "Testing skip if unequal function - equal"
        main.skip_if_unequal(5, 0x40)
        self.assertEqual(main.PC, 0x204)
        print "Skip if unequal - equal passed."

    def test_register_compare(self):
        print
        print "Testing two register comparison function"

        #This section is repeat to ensure register is cleared and then set.
        #Register A
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x40)
        self.assertEqual(main.registers[5], 0x40)

        #Register B - equal to A
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x40)
        self.assertEqual(main.registers[10], 0x40)

        #Register B - Unequal
        self.assertEqual(main.registers[9], 0)
        main.set_register(9, 0x50)
        self.assertEqual(main.registers[9], 0x50)

        main.register_equal_skip(5, 10)
        self.assertEqual(main.PC, 0x202)
        print "Two register comparison - equal passed."

        main.register_equal_skip(5, 9)
        self.assertEqual(main.PC, 0x202)
        print "Two register comparison - unequal passed."

    def test_register_add(self):
        print
        print "Testing addition to register function"
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x40)
        self.assertEqual(main.registers[5], 0x40)

        main.register_add_value(5, 0x10)
        self.assertEqual(main.registers[5], 0x50)
        print "Addition to register passed."

    def test_register_ab(self):
        print
        print "Testing setting register to value of register b function"
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x40)
        self.assertEqual(main.registers[5], 0x40)
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x20)
        self.assertEqual(main.registers[10], 0x20)

        main.register_a_b_set(5, 10)
        self.assertEqual(main.registers[5], 0x20)
        print "Register a assignment passed."
        self.assertEqual(main.registers[10], 0x20)
        print "Register b passed."

    def test_register_OR(self):
        print
        print "Testing OR on two registers function"
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x3C)
        self.assertEqual(main.registers[5], 0x3C)
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x42)
        self.assertEqual(main.registers[10], 0x42)

        main.or_register(5, 10)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.registers[10], 0x42)
        print "OR on registers passed."

    def test_register_AND(self):
        print
        print "Testing OR on two registers function"
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x3C)
        self.assertEqual(main.registers[5], 0x3C)
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x42)
        self.assertEqual(main.registers[10], 0x42)

        main.and_register(5, 10)
        self.assertEqual(main.registers[5], 0x00)
        self.assertEqual(main.registers[10], 0x42)
        print "AND on registers passed."

    def test_register_XOR(self):
        print
        print "Testing OR on two registers function."
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x3C)
        self.assertEqual(main.registers[5], 0x3C)
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x42)
        self.assertEqual(main.registers[10], 0x42)

        main.xor_register(5, 10)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.registers[10], 0x42)
        print "XOR on registers passed."

    def test_register_add(self):
        print
        print "Testing adding register to another function."
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x7e)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x42)
        self.assertEqual(main.registers[10], 0x42)
        self.assertEqual(main.registers[15], 0x00)

        main.add_two_registers(5, 10)
        self.assertEqual(main.registers[5], 0xC0)
        print "Adding registers - no carry passed"

        #TODO - If I carry, I can't store anything over 255 in a register, right?
        #       255 in one byte? Yes, I only store the remainder in the register
        main.add_two_registers(5, 10)
        self.assertEqual(main.registers[5], 0x02)
        self.assertEqual(main.registers[15], 0x01)
        print "Adding registers - carry passed"

    def test_register_minus(self):
        print
        print "Testing subtracting one register from another function."
        main.set_register(5, 0x7e)
        main.set_register(10, 0x42)

        main.registers_subtract(5, 10)
        self.assertEqual(main.registers[5], 0x3C)
        self.assertEqual(main.registers[15], 0x01)
        print "Subtraction - no borrow passed."

        #TODO - I can't put a negative value into a register can I???
        main.registers_subtract(5, 10)
        self.assertEqual(main.registers[5], 0x6)
        self.assertEqual(main.registers[15], 0x00)
        print "Subtraction - borrow passed."

    def test_shift_right(self):
        print
        print "Testing shift right function."
        main.set_register(5, 0x7e)

        main.shift_right(5)
        self.assertEqual(main.registers[5], 0x3F)
        print "The shift right function passed"

    def test_shift_left(self):
        print
        print "Testing shift left function."
        main.set_register(5, 0x8e)
        main.shift_left(5)
        self.assertEqual(main.registers[5], 0x1C)
        print "Shift left - greater than 128 passed"

        main.set_register(5, 0x7e)
        main.shift_left(5)
        self.assertEqual(main.registers[5], 0xFC)
        print "Shift left - less than 128 passed"


    def test_unequalreg_skip(self):
        print
        print "Testing if unequal registers skip function."
        main.set_register(5, 0x7e)
        main.set_register(10, 0x42)

        main.register_unequal_skip(5, 10)
        self.assertEqual(main.PC, 0x202)
        print "Skip if unequal registers - unequal passed."

        main.set_register(10, 0x7e)
        self.assertEqual(main.registers[10], 0x7e)

        main.register_unequal_skip(5, 10)
        self.assertEqual(main.PC, 0x202)
        print "Skip if unequal registers - equal passed"

    def test_set_I(self):
        print
        print "Testing setting I function."
        self.assertEqual(main.I, 0x00)
        #TODO - Is this an address in the memory? yes
        main.set_I(0x0F)
        self.assertEqual(main.I, 0x0F)
        print "Setting I passed"

    def test_jump_first_reg(self):
        print
        print "Testing add first register to PC function."
        self.assertEqual(main.registers[0], 0)
        main.set_register(0, 0x7e)
        self.assertEqual(main.registers[0], 0x7e)

        main.jump_first_reg(4)
        self.assertEqual(main.PC, 0x82)
        print "Jump to value + register passed"

    def test_jump_random(self):
        print
        print "Testing random jump function."
        self.assertEqual(main.registers[5], 0)
        main.jump_random(5, 0x64)
        #TODO - Check not above I + 255 and then perhaps loop to test a few
        self.assertNotEqual(main.registers[5], 0x64)
        print "Random jump passed"

    def test_setto_delaytimer(self):
        print
        print "Testing set register to delay timer value function."
        main.set_register(5, 0x7e)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.delay_timer, 0x00)
        main.set_reg_to_delay(5)
        self.assertEqual(main.registers[5], 0x00)
        print "Register set to delay timer passed"

    #TODO - Input_to_register_test

    def test_set_delay_timer(self):
        print
        print "Testing setting delay timer function."
        main.set_register(5, 0x7e)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.delay_timer, 0x00)
        main.set_delay_timer(5)
        self.assertEqual(main.delay_timer, 0x7e)
        print "Delay timer set passed"

    def test_set_sound_timer(self):
        print
        print "Testing setting sound timer function."
        main.set_register(5, 0x7e)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.sound_timer, 0x00)
        main.set_sound_timer(5)
        self.assertEqual(main.sound_timer, 0x7e)
        print "Sound timer set passed"

    def test_stack_add(self):
        print
        print "Testing the addition to I"
        main.set_I(0x7e)
        self.assertEqual(main.I, 0x7E)
        main.set_register(5, 0x0F)
        self.assertEqual(main.registers[5], 0x0F)

        main.add_to_stack(5)
        self.assertEqual(main.I, 0x8D)
        print "Addition to I has passed"

    def test_sprite(self):
        print
        print "Testing the location of sprites function"
        main.set_register(5, 7)
        main.sprite(5)
        self.assertEqual(main.I, 0x23)
        print "The sprite location function passed"


    def test_memory_store(self):
        print
        print "Testing memory store function."
        main.set_I(0x802)

        main.set_register(0, 0x0A)
        main.set_register(1, 0x0B)
        main.set_register(2, 0x0C)
        main.set_register(3, 0x0D)
        main.set_register(4, 0x0E)

        main.store_reg_in_mem(4)
        count = 0
        for i in range(main.I, 5):
            self.assertEqual(memory[i], registers[count])
            count + 1
        self.assertEqual(main.I, 0x802)
        print "Memory store has passed"

    def test_memory_read(self):
        print
        print "Testing memory read into registers function."
        main.set_I(0x802)
        main.memory[0x802] = 0x01
        main.memory[0x803] = 0x02
        main.memory[0x804] = 0x03

        main.read_from_memory(0x806)
        self.assertEqual(main.registers[0], 0x01)
        self.assertEqual(main.registers[1], 0x02)
        self.assertEqual(main.registers[2], 0x03)
        print "Memory read function has passed"

if __name__ == '__main__':
    unittest.main()
