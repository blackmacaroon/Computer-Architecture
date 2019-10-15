"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256   #random access memory = 256 bits     list of 256 zeros
        self.reg = [0] * 8     #registries = 8   list of 8 zeros
        self.PC = 0            #program counter
        self.IR = 0            #internal registers, if we need them
        
    #MAR = memory address register
    #accept the ADDRESS to read and return the value stored there
    def ram_read(self, MAR):
        # print("ram read", MAR)
        return self.ram[MAR]
        
    #MDR = memory data register
    #accept the VALUE/DATA to write, and the ADDRESS to write it to
    def ram_write(self, MDR, MAR):
        # print("ram write", MDR)
        self.ram[MAR] = MDR

    def load(self, file_name):
        """Load a program into memory."""

        address = 0
        program = []
        if file_name is None:
            print("error.")  # for stretch
            sys.exit(1)
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    # Process comments:
                    # Ignore anything after a # symbol
                    comment_split = line.split("#")
                    # Convert any numbers from binary strings to integers
                    num = comment_split[0]
                    try:
                        x = int(num, 2)
                    except ValueError:
                        continue
                    # print in binary and decimal
                    print(f"{x:08b}: {x:d}")
                    program.append(x)
        except ValueError:
            print(f"File not found")

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        # elif op == "MUL":
        #     self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #read the memory address that's stored in register `PC`
        running = True
        
        while running:
            # self.trace()
            IR = self.ram[self.PC]  #IR = instruction register
            # operand_a = self.ram_read(self.PC+1)
            # operand_b = self.ram_read(self.PC+2)
            LDI = 0b10000010
            PRN = 0b01000111
            HLT = 0b00000001
            MUL = 0b10100010
            
            # set the value from the register to an integer
            # print("IR", IR)
            # print("op A", operand_a)
            # print("op B", operand_b)
            if IR == LDI:
                reg_a = self.ram[self.PC + 1]
                reg_b = self.ram[self.PC + 2]
                self.reg[reg_a] = [reg_b]
                self.PC += 3
            #Print to the console the decimal integer value stored in the given register
            elif IR == PRN:
                reg_a = self.ram[self.PC + 1]
                print(f"print value: {self.reg[reg_a]}")
                self.PC += 2
                #halt! and exit
            elif IR == MUL:  # MUL
                reg_a = self.ram[self.PC + 1]
                reg_b = self.ram[self.PC + 2]
                self.reg[reg_a] *= self.reg[reg_b]
                # self.alu("MUL", reg_a, reg_b)
                self.PC += 3
            elif IR == HLT:
                running = False
                self.PC += 1
            else:
                print(f"Unknown Instruction: {IR}")
                sys.exit(1)