def s_type(unit, idx):

    opcode = "0100011"
    funct3 = "010"

    # expected format: sw rs2 imm(rs1)
    if(len(unit) != 3):
        raise ValueError(f"Line {idx}: Invalid sw syntax")

    _, rs2, mem = unit

    imm = int(mem.split("(")[0])
    rs1 = mem.split("(")[1][:-1]

    if(rs1 not in reg_map or rs2 not in reg_map):
        raise ValueError(f"Line {idx}: Invalid register")

    # convert negative immediate
    if(imm < 0):
        imm = (1 << 12) + imm

    imm_bin = format(imm, "012b")

    # split immediate as required by S-type format
    imm_11_5 = imm_bin[:7]
    imm_4_0  = imm_bin[7:]

    rs1_bin = format(reg_map[rs1], "05b")
    rs2_bin = format(reg_map[rs2], "05b")

    # final instruction format
    return imm_11_5 + rs2_bin + rs1_bin + funct3 + imm_4_0 + opcode