branch_map={"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}

reg_map = {
"zero":0,"ra":1,"sp":2,"gp":3,"tp":4,
"t0":5,"t1":6,"t2":7,
"s0":8,"s1":9,
"a0":10,"a1":11,"a2":12,"a3":13,"a4":14,"a5":15,"a6":16,"a7":17,
"s2":18,"s3":19,"s4":20,"s5":21,"s6":22,"s7":23,"s8":24,"s9":25,"s10":26,"s11":27,
"t3":28,"t4":29,"t5":30,"t6":31
}

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
