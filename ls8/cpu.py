"""CPU functionality."""
import sys
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        
        self.ram = [0] * 256
        self.register = [0] * 8
        self.PC = 0
        self.SPL = 7
        
    def load(self):
        """Load a program into memory."""
        address = 0
        # program = []
        
        # if sys.argv[1] is None:
        #     print("This file is bad.")  # for stretch
        #     sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    if line[0] != "#" and line != "\n":
                        self.ram[address] = int(line[:8], 2)
                        address += 1
                f.closed
                    # Process comments:
                    # Ignore anything after a # symbol
                    # comment_split = line.split("#")
                    # # Convert any numbers from binary strings to integers
                    # num = comment_split[0]
                    # try:
                    #     x = int(num, 2)
                    # except ValueError:
                    #     continue
                    # # print in binary and decimal
                    # print(f"{x:08b}: {x:d}")
                    # program.append(x)
        except ValueError:
            print(f"File not found")
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, MAR):
        return self.ram[MAR]
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
    # def handle_push(self):
    # def handle_pop(self):
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.register[i], end='')
        print()
    def run(self):
        """Run the CPU."""
        PRN = 0b01000111
        HLT = 0b00000001
        LDI = 0b10000010
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        running = True
        while running:
            IR = self.ram[self.PC]
            operandA = self.ram_read(self.PC + 1)
            operandB = self.ram_read(self.PC + 2)
            if IR == LDI:
                # operandA = self.ram_read(self.PC + 1)
                # operandB = self.ram_read(self.PC + 2)
                self.register[operandA] = operandB
                self.PC += 3
            elif IR == PRN:
                print(self.register[operandA])
                self.PC += 2
            elif IR == HLT:
                running = False
                self.PC += 1
            elif IR == MUL:
                self.alu("MUL", operandA, operandB)
                self.PC += 3
            elif IR == POP:
                self.register[operandA] = self.ram[self.SPL]
                self.SPL += 1
                self.PC += 2
            elif IR == PUSH:
                self.SPL -= 1
                self.ram[self.SPL] = self.register[operandA]
                self.PC += 2

            else:
                print(f"Unknown Instruction {IR}")
                sys.exit(1)