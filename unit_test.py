import unittest
import main

#TODO - QUESTION - Can I just assign two of the registers a value in the setup
#                  so I don't have to keep checking they're zero, setting them,
#                  and then performing a function on them?

#       QUESTION - Why am I having to make PC global in all my functions but not
#                  the registers array?

class Test_Chip_8(unittest.TestCase):
    def setUp(self):
        main.PC = 0x300 # not 0x200, to check execution that's partially into and not validate only fresh executions
        main.stack = []
        main.registers = [0x00 for x in range(0x10)]
        main.I = 0
        main.clear_memory()

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
        self.assertEqual(main.stack[0], 0x300)
        self.assertEqual(main.PC, 0x400)
        print "jump to subroutine passed."
        print
        print "Testing return from subroutine function"
        main.return_address()
        self.assertEqual(len(main.stack), 0)
        self.assertEqual(main.PC, 0x300)
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
        self.assertEqual(main.PC, 0x302)
        print "Skip if equal - equal passed."
        print
        print "Testing skip if equal function - unequal"
        main.skip_if_equal(5, 0x50)
        self.assertEqual(main.PC, 0x302)
        print "Skip if equal - unequal passed."
        print
        print "Testing skip if unequal function - unequal"
        main.skip_if_unequal(5, 0x50)
        self.assertEqual(main.PC, 0x304)
        print "Skip if unequal - unequal passed."
        print
        print "Testing skip if unequal function - equal"
        main.skip_if_unequal(5, 0x40)
        self.assertEqual(main.PC, 0x304)
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
        self.assertEqual(main.PC, 0x302)
        print "Two register comparison - equal passed."

        main.register_equal_skip(5, 9)
        self.assertEqual(main.PC, 0x302)
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
        #       255 in one byte?
        main.add_two_registers(5, 10)
        self.assertEqual(main.registers[5], 0x102)
        self.assertEqual(main.registers[15], 0x01)
        print "Adding registers - carry passed"

    def test_register_minus(self):
        print
        print "Testing subtracting one register from another function."
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x7e)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x42)
        self.assertEqual(main.registers[10], 0x42)
        self.assertEqual(main.registers[15], 0x00)

        main.registers_subtract(5, 10)
        self.assertEqual(main.registers[5], 0x3C)
        self.assertEqual(main.registers[15], 0x01)
        print "Subtraction - no borrow passed."

        #TODO - I can't put a negative value into a register can I???
        main.registers_subtract(5, 10)
        self.assertEqual(main.registers[5], 0x6)
        self.assertEqual(main.registers[15], 0x00)
        print "Subtraction - borrow passed."

    def test_unequalreg_skip(self):
        print
        print "Testing if unequal registers skip function."
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x7e)
        self.assertEqual(main.registers[5], 0x7e)
        self.assertEqual(main.registers[10], 0)
        main.set_register(10, 0x42)
        self.assertEqual(main.registers[10], 0x42)

        main.register_unequal_skip(5, 10)
        self.assertEqual(main.PC, 0x302)
        print "Skip if unequal registers - unequal passed."

        main.set_register(10, 0x7e)
        self.assertEqual(main.registers[10], 0x7e)

        main.register_unequal_skip(5, 10)
        self.assertEqual(main.PC, 0x302)
        print "Skip if unequal registers - equal passed."








































if __name__ == '__main__':
    unittest.main()
