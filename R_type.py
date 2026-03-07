def r_type(unit, idx):
 # funct7 values for R-type instructions
    funct7_map = {"add":"0000000","sub":"0100000","sll":"0000000","slt":"0000000",
                  "sltu":"0000000","xor":"0000000","srl":"0000000","or":"0000000","and":"0000000"}
 # funct3 values select ALU operation
    funct3_map = {"add":"000","sub":"000","sll":"001","slt":"010",
                  "sltu":"011","xor":"100","srl":"101","or":"110","and":"111"}

    opcode = "0110011"       # opcode for all R-type instructions
 # R-type format must have 4 tokens
    if(len(unit) != 4):
        raise ValueError(f"Line {idx}: Invalid R-type syntax")

    op, rd, rs1, rs2 = unit

    if(rd not in reg_map or rs1 not in reg_map or rs2 not in reg_map):
        raise ValueError(f"Line {idx}: Invalid register")
 # convert registers to 5-bit binary
    rd_bin  = format(reg_map[rd], "05b")
    rs1_bin = format(reg_map[rs1], "05b")
    rs2_bin = format(reg_map[rs2], "05b")

    funct7 = funct7_map[op]
    funct3 = funct3_map[op]

 # final 32-bit instruction layout
    return funct7 + rs2_bin + rs1_bin + funct3 + rd_bin + opcode

