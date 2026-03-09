import sys

R_TYPE = {"add","sub","sll","slt","sltu","xor","srl","or","and"}
I_TYPE = {"lw","addi","sltiu","jalr"}
S_TYPE = {"sw"}
B_TYPE = {"beq","bne","blt","bge","bltu","bgeu"}
U_TYPE = {"lui","auipc"}
J_TYPE = {"jal"}

all_mnemonics = []
all_mnemonics += list(R_TYPE)
all_mnemonics += list(I_TYPE)
all_mnemonics += list(S_TYPE)
all_mnemonics += list(B_TYPE)
all_mnemonics += list(U_TYPE)
all_mnemonics += list(J_TYPE)

def r_type(unit, idx):
    return

def i_type(unit, PC, labels, idx):
    return

def s_type(unit, idx):
    return

def b_type(unit, PC, labels, idx):
    return

def u_type(unit, idx):
    return

def j_type(unit, PC, labels, idx):
    return

def final_halt(unit):
    return (len(unit) == 4 and unit[0] == "beq" and unit[1] == "zero" and 
        unit[2] == "zero" and unit[3] in {"0","0x0","0x00000000"})

# Finds the label in the instruction and seperates it from the rest of the instruction if found
def label_finding(line):
    if(":" not in line):    # IF there is no label in the line
        return None, line.strip()

    left, right = line.split(":", 1)    # IF there is label in the line
    label = left.strip()    #label
    rest = right.strip()    #rest of the instruction
    return label, rest

# Splits each instruction
def listing(instr):
    instr = instr.replace(",", " ")
    return instr.split()

# Read the whole instruction set and makes a dictionary of label as key and their memory addresses as values
def label_table(lines):
    PC = 0
    labels = {}

    idx = 1
    for line in lines:
        label, rest = label_finding(line)

        if(label != None):      #if there is any label in the instruction
            if(not label or not label[0].isalpha()):    # Checking that label is not empty as well as starts with alphabet
                raise ValueError(f"Invalid label {label} in line {idx}")
            
            if(label in labels):        # No same label should be present
                raise ValueError(f"Same label {label} in line {idx}")
            
            labels[label] = PC

        if(rest != ""):     # Updating the PC if instuction is not empty
            PC += 4
        
        idx += 1        # Updating the line of instruction
    return labels

# Converts all assembly instructions into 32-bits machine code
def assemble(lines, labels):
    PC = 0
    output_lines = []

    idx = 1
    for line in lines:
        label, rest = label_finding(line)

        if(rest == ""):     # Skipping the empty line
            idx += 1
            continue

        unit = listing(rest)    # Getting list of each instruction line
        mnemonic = unit[0]      # The main diffentiating operation

        if(mnemonic not in all_mnemonics):      # For any unknown instruction
            raise ValueError(f"Unknown instruction {mnemonic} at line {idx}")

        # Identifing the correct instruction type and calling it
        if(mnemonic in R_TYPE):
            bin32 = r_type(unit, idx)

        elif mnemonic in I_TYPE:
            bin32 = i_type(unit, PC, labels, idx)

        elif mnemonic in S_TYPE:
            bin32 = s_type(unit, idx)

        elif mnemonic in B_TYPE:
            if unit[3] in labels:
                off = labels[unit[3]] - PC
            else:
                off = int(unit[3], 0)  # allows decimal immediate

            bin32 = b_type(unit[0], unit[1], unit[2], off)
            if bin32 is None:
                raise ValueError(f"Invalid branch encoding line {idx}")
            
        elif mnemonic in U_TYPE:
            bin32 = u_type(unit[0], unit[1], int(unit[2]))

        elif mnemonic in J_TYPE:

            if(unit[2] not in labels):
                raise ValueError(f"Unknown label {unit[2]} at line {idx}")

            offset = labels[unit[2]] - PC        # Finding the new memory address
            bin32 = j_type(unit[1], offset)

        if(len(bin32) != 32):
            raise ValueError(f"Encoder must return 32-bit binary string at line {idx}")

        output_lines.append(bin32)
        PC += 4
        idx += 1
    return output_lines


# using sys instead of input()
if len(sys.argv) < 2:
    print("Usage: python assembler.py <input_file>")
    sys.exit()

input_file = sys.argv[1]

with open(input_file, "r") as f:        #reading the file
    lines = f.readlines()

lines = [ln.strip() for ln in lines if ln.strip() != ""]        #removes spaces and newline characters and removes blank lines too
labels = label_table(lines)     #dictionary with label as key and it's corresponding PC value as key

instruction_lines = []      #this will contain only the instructions, without any label

# Keeps only the actual instructions
for line in lines:
    l, rest = label_finding(line)
    if(rest != ""):
        instruction_lines.append(rest)

# Checking if there are only label and not any instructions Eg:- loop:
if(not instruction_lines):
    print("No instructions found")
    sys.exit()

# Checking if the last instruction is HALT or not
if(not final_halt(listing(instruction_lines[-1]))):
    print("Virtual Halt missing or not last")
    sys.exit()

try:
    out_lines = assemble(instruction_lines, labels)
    for line in out_lines:
        print(line)
except Exception as e:
    print(str(e))