# commands
PRINT_BEEJ = 1  # putting a one as an argument for the opcode will make it run the 1 as an operation
HALT = 2
PRINT_NUM = 3
SAVE = 4  # Save value into register
PRINT_REGISTER = 5
ADD = 6

# opcodes take the next item as an argument
memory = [
    PRINT_BEEJ,
    SAVE,  # SAVE 65 into R2
    65,
    2,
    SAVE,  # Save 20 into R3
    20,
    3,
    ADD,   # Add R2 + R3 = 65 + 20, store in R2
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT,

]  # memory address


pc = 0  # program counter
running = True

# Create 8 registers
register = [0] * 8

while running:
    command = memory[pc]  # points at our memory address - The R or the read

    if command == PRINT_BEEJ:
        print("BEEJ")
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2  # since we have two bytes, we add 2 - the counter depends on how many arguments there are for each action

    elif command == HALT:
        running = False
        pc += 1

    elif command == SAVE:
        num = memory[pc + 1]  # Gets the number from the first argument
        reg = memory[pc + 2]  # Get the register index from the second argument
        register[reg] = num  # Store the number in the right register
        pc += 3  # because we have two arguments + the command

    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]  # get the register index from the first arg
        print(register[reg])  # print content of that register
        pc += 2

    elif command == ADD:
        reg_a = memory[pc+1]   # Get the 1st register index from 1st arg
        reg_b = memory[pc+2]   # Get the 2nd register index from 2nd arg
        register[reg_a] += register[reg_b]  # Add registers, store in reg_a
        pc += 3

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)