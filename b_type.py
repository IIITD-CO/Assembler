branch_map={"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}

def b_type(inst, r1, r2, off):

    opcode = "1100011"

    rs1 = format(reg_map[r1], "05b")
    rs2 = format(reg_map[r2], "05b")

    funct3 = branch_map[inst]

    if off % 2 != 0:
        raise ValueError("Branch offset must be even")

    if off < -4096 or off > 4094:
        raise ValueError("branch immediate out of range")

    if off < 0:
        off = (1 << 13) + off

    imm = format(off, "013b")

    imm12 = imm[0]
    imm10_5 = imm[2:8]
    imm4_1 = imm[8:12]
    imm11 = imm[1]

    return imm12 + imm10_5 + rs2 + rs1 + funct3 + imm4_1 + imm11 + opcode
