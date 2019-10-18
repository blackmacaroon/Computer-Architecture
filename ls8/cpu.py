"""CPU functionality."""
import sys
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        
        self.ram = [0] * 256
        self.register = [0] * 8
        self.PC = 0
        self.SPL = 7   #points to register 7  aka 0xF4
        self.flags = 0b00000000 # register made of 8 bits 'FL' bits: 0b00000LGE
    
        
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
        """ALU operations -- ARITHMETIC LOGIC UNIT"""
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]
        elif op == "CMP":  #compare
            # * If registerA is less than registerB, set the Less-than `L` flag to 1,
            #   otherwise set it to 0.
            if reg_a < reg_b:
                self.flags == 0b00000100
            # * If registerA is greater than registerB, set the Greater-than `G` flag
            #   to 1, otherwise set it to 0.
            elif reg_a > reg_b:
                self.flags == 0b00000010
            #* If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
            elif reg_a == reg_b:
                self.flags == 0b00000001
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
        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
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
            elif IR == ADD:
                self.alu("ADD", operandA, operandB)
                self.PC += 3
            elif IR == SUB:
                self.alu("SUB", operandA, operandB)
                self.PC += 3
            elif IR == MUL:
                self.alu("MUL", operandA, operandB)
                self.PC += 3
            elif IR == DIV:
                self.alu("DIV", operandA, operandB)
                self.PC += 3
            elif IR == CMP:
                self.alu("CMP", operandA, operandB)
                self.PC += 3
            elif IR == POP:
                # copy the value from the address pointed to by the SP, to the given register
                self.register[operandA] = self.ram[self.SPL]
                # increment pointer location
                self.SPL += 1
                self.PC += 2
            elif IR == PUSH:
                self.SPL -= 1
                self.ram[self.SPL] = self.register[operandA]
                self.PC += 2
            elif IR == CALL:
                self.register[self.SPL] -= 1
                self.ram[self.SPL] = self.PC +2
                self.PC = self.register[operandA]
            elif IR == RET:
                self.PC = self.ram[self.SPL]
                self.register[self.SPL] += 1
            elif IR == JMP:
                # Jump to the address stored in the given register
                # Set the `PC` to the address stored in the given register
                self.PC = self.register[operandA]  # A is the address, not the pointer, send the counter to the given address
            # flags 00000LGE
            elif IR == JEQ:
                # If `equal` flag is set (true)
                if self.flags == 0b00000001:
                    # jump to the address stored in the given register
                    self.PC = self.register[operandA]
                #otherwise, skip to the next instruction PC += 2
                else:
                    self.PC += 2
                
            elif IR == JNE:
                # If `E` flag is clear (false, 0)
                if self.flags == 0b00000000:
                    #jump to the address stored in the given register
                    self.PC = self.register[operandA]
                # otherwise, skip to the next instruction PC += 2
                else:
                    self.PC += 2
                
                

            else:
                print(f"Unknown Instruction {IR}")
                sys.exit(1)