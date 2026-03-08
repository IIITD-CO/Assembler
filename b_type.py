def b_type(inst,r1,r2,off):

    opcode="1100011"

    # convertd the  register names to 5-bits binary using the  reg_map
    rs1=format(reg_map[r1],"05b")
    rs2=format(reg_map[r2],"05b")

    funct3=branch_map[inst]

    # branch offsets must be multiples of 2
    if off % 2 != 0:
        raise ValueError("Branch offset must be even")

    # correct byte range
    if off < -4096 or off > 4094:
        raise ValueError("branch immediate out of range")
    
    off = off >> 1

    if off<0:
        off=(1<<12)+off

    imm=format(off,"012b")  # converting the  offset to 12-bits binary

    out = imm[0] + imm[2:8] + rs2 + rs1 + funct3 + imm[8:12] + imm[1] + opcode

    return out