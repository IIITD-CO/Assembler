import sys

from R_type import r_type
from I_type import i_type
from s_type import s_type
from b_type import b_type
from u_type import u_type
from j_type import j_type


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


def final_halt(unit):
    return (
        len(unit) == 4 and
        unit[0] == "beq" and
        unit[1] in {"zero","x0"} and
        unit[2] in {"zero","x0"} and
        unit[3] in {"0","0x0","0x00000000"}
    )

def label_finding(line):
    if ":" not in line:
        return None, line.strip()

    left, right = line.split(":", 1)
    label = left.strip()
    rest = right.strip()

    return label, rest


def listing(instr):
    instr = instr.replace(",", " ")
    return instr.split()


def label_table(lines):
    PC = 0
    labels = {}

    idx = 1
    for line in lines:
        label, rest = label_finding(line)

        if label is not None:

            if not label or not label[0].isalpha():
                raise ValueError(f"Invalid label {label} in line {idx}")

            if label in labels:
                raise ValueError(f"Same label {label} in line {idx}")

            labels[label] = PC

        if rest != "":
            PC += 4

        idx += 1

    return labels


def assemble(lines, labels):

    PC = 0
    output_lines = []

    for idx, line in lines:

        rest = line

        if rest == "":
            continue

        unit = listing(rest)
        mnemonic = unit[0]

        if mnemonic not in all_mnemonics:
            raise ValueError(f"Unknown instruction {mnemonic} at line {idx}")

        if mnemonic in R_TYPE:
            bin32 = r_type(unit, idx)

        elif mnemonic in I_TYPE:
            bin32 = i_type(unit, PC, labels, idx)

        elif mnemonic in S_TYPE:
            bin32 = s_type(unit, idx)

        elif mnemonic in B_TYPE:

            if unit[3] in labels:
                off = labels[unit[3]] - PC
            else:
                off = int(unit[3], 0)

            bin32 = b_type(unit[0], unit[1], unit[2], off)

            if bin32 is None:
                raise ValueError(f"Invalid branch encoding line {idx}")

        elif mnemonic in U_TYPE:
            bin32 = u_type(unit[0], unit[1], int(unit[2]))

        elif mnemonic in J_TYPE:

            if unit[2] not in labels:
                raise ValueError(f"Unknown label {unit[2]} at line {idx}")

            offset = labels[unit[2]] - PC
            bin32 = j_type(unit[1], offset)

        if len(bin32) != 32:
            raise ValueError(f"Encoder must return 32-bit binary string at line {idx}")

        output_lines.append(bin32)

        PC += 4

    return output_lines


# -------------------------
# Input handling
# -------------------------

if len(sys.argv) >= 3:

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        lines = f.readlines()

    write_to_file = True

else:

    lines = sys.stdin.readlines()
    write_to_file = False


lines = [ln.strip() for ln in lines if ln.strip() != ""]


def write_error(msg):

    if write_to_file:
        with open(output_file, "w") as f:
            f.write(msg + "\n")
    else:
        print(msg)

    sys.exit()


try:
    labels = label_table(lines)
except Exception as e:
    write_error(str(e))


instruction_lines = []

for i in range(len(lines)):
    l, rest = label_finding(lines[i])

    if rest != "":
        instruction_lines.append((i + 1, rest))


if not instruction_lines:
    write_error("No instructions found")


if not final_halt(listing(instruction_lines[-1][1])):
    write_error("Virtual Halt missing or not last")


try:

    out_lines = assemble(instruction_lines, labels)

    if write_to_file:

        with open(output_file, "w") as f:
            for line in out_lines:
                f.write(line + "\n")

    else:

        for line in out_lines:
            print(line)

except Exception as e:
    write_error(str(e))
