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
    if(":" not in line):
        return None, line.strip()

    left, right = line.split(":", 1)
    label = left.strip()
    rest = right.strip()
    return label, rest

# Splits each instruction
def listing(instr):
    instr = instr.replace(",", " ")
    return instr.split()

# Read the whole instruction set and makes a dictionary of labels with their memory addresses after each instruction
def label_table(lines):
    PC = 0
    labels = {}

    idx = 1
    for line in lines:
        label, rest = label_finding(line)

        if(label != None):
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
            bin32 = b_type(unit, PC, labels, idx)
        elif mnemonic in U_TYPE:
            bin32 = u_type(unit[0], unit[1], int(unit[2]))
        elif mnemonic in J_TYPE:
            rd_name = unit[1]
            target = unit[2]

            if(target not in labels):
                raise ValueError(f"Unknown label {target} at line {idx}")

            offset = labels[target] - PC        # Finding the new memory address
            bin32 = j_type(PC, rd_name, offset)

        if(len(bin32) != 32):
            raise ValueError(f" Encoder must return 32-bit binary string at line {idx}")

        output_lines.append(bin32)
        PC += 4

    return output_lines

input_file = input("Enter input file: ")

with open(input_file, "r") as f:
    lines = f.readlines()

lines = [ln.strip() for ln in lines if ln.strip() != ""]
labels = label_table(lines)

instruction_lines = []

# Keeps only the actual instructions
for line in lines:
    l, rest = label_finding(line)
    if(rest != ""):
        instruction_lines.append(rest)

# Checking if there are instructions or not
if(not instruction_lines):
    print("No instructions found")
    exit()

# Checking if the last instruction is HALT or not
if(not final_halt(listing(instruction_lines[-1]))):
    print("Virtual Halt missing or not last")
    exit()

try:
    out_lines = assemble(lines, labels)
    for line in out_lines:
        print(line)
except Exception as e:
    print(str(e))