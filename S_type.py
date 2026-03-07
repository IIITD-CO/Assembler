def s_type(unit, idx):
    if len(unit) != 3:  #syntax error check
        raise ValueError(f"Line {idx}: Invalid syntax")

    opcode = "0100011" #predefined
    funct3 = "010"
    
    rs2 = unit[1]

    temp = unit[2]    #taking 2nd position value in temp
    parts = temp.split("(")    #splitting
    imm = int(parts[0])    #imm value gets by splitting
    rs1 = parts[1][:-1]    #gets rs1 value
    
    if rs1 not in reg_map:  #invalid register check
        raise ValueError(f"Line {idx}: Invalid register")

    if rs2 not in reg_map:  #invalid register check
        raise ValueError(f"Line {idx}: Invalid register")

    if imm < 0:     #if imm is negative no.
        imm = (1 << 12) + imm

    imm_bin = format(imm, "012b")  #converting to binary
    imm_11_5 = imm_bin[:7]         #first seven bits
    imm_4_0 = imm_bin[7:]          #after seven bits

    rs1_bin = format(reg_map[rs1], "05b")  #converting to binary
    rs2_bin = format(reg_map[rs2], "05b")

    return imm_11_5 + rs2_bin + rs1_bin + funct3 + imm_4_0 + opcode   #final output
