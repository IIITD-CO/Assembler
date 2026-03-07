def r_type(unit, idx):

    # funct7 values
    funct7_map = {"add":"0000000","sub":"0100000","sll":"0000000","slt":"0000000",
                  "sltu":"0000000","xor":"0000000","srl":"0000000","or":"0000000","and":"0000000"}

    # funct3 values
    funct3_map = {"add":"000","sub":"000","sll":"001","slt":"010",
                  "sltu":"011","xor":"100","srl":"101","or":"110","and":"111"}

    opcode = "0110011"   # opcode for r type instructions

    # r type instruction should have 4 parts
    if len(unit) != 4:
        raise ValueError("Line " + str(idx) + ": invalid r type instruction")

    op = unit[0]
    rd = unit[1]
    rs1 = unit[2]
    rs2 = unit[3]

    # checking registers
    if rd not in reg_map:
        raise ValueError("Line " + str(idx) + ": invalid register")

    if rs1 not in reg_map:
        raise ValueError("Line " + str(idx) + ": invalid register")

    if rs2 not in reg_map:
        raise ValueError("Line " + str(idx) + ": invalid register")

    # convert registers to binary
    rd_bin = format(reg_map[rd], "05b")
    rs1_bin = format(reg_map[rs1], "05b")
    rs2_bin = format(reg_map[rs2], "05b")

    funct7 = funct7_map[op]
    funct3 = funct3_map[op]

    # combine everything
    final_inst = funct7 + rs2_bin + rs1_bin + funct3 + rd_bin + opcode

    return final_inst
