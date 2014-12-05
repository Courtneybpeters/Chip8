import unittest
import main

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


    def test_registers(self):
        print
        print "Testing register assignment function"
        self.assertEqual(main.registers[5], 0)
        main.set_register(5, 0x40)
        self.assertEqual(main.registers[5], 0x40)
        print "register assignment passed."
        print
        print "Testing skip if equal function"
        main.registers[5] = 0x40
        main.skip_if_equal(5, 0x40)
        self.assertEqual(main.PC, 0x300)
        print "Skip if equal passed."


if __name__ == '__main__':
    unittest.main()
