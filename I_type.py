def i_type(unit, PC, labels, idx):

    # funct3 and opcode values
    funct3_map = {
        "lw":"010",
        "addi":"000",
        "sltiu":"011",
        "jalr":"000"
    }

    opcode_map = {
        "lw":"0000011",
        "addi":"0010011",
        "sltiu":"0010011",
        "jalr":"1100111"
    }

    op = unit[0]

    # lw uses special memory format imm(rs1)
    if(op == "lw"):

        if(len(unit) != 3):
            raise ValueError(f"Line {idx}: Invalid lw syntax")

        rd = unit[1]

        mem = unit[2]
        imm = int(mem.split("(")[0])
        rs1 = mem.split("(")[1][:-1]

    else:

        # other I-type instructions
        if(len(unit) != 4):
            raise ValueError(f"Line {idx}: Invalid I-type syntax")

        rd = unit[1]
        rs1 = unit[2]
        imm = int(unit[3])

    if(rd not in reg_map or rs1 not in reg_map):
        raise ValueError(f"Line {idx}: Invalid register")

    # convert negative immediate using 2's complement
    if(imm < 0):
        imm = (1 << 12) + imm

    imm_bin = format(imm, "012b")

    rs1_bin = format(reg_map[rs1], "05b")
    rd_bin  = format(reg_map[rd], "05b")

    funct3 = funct3_map[op]
    opcode = opcode_map[op]

    # final encoding
    return imm_bin + rs1_bin + funct3 + rd_bin + opcode