reg_map = {
    "zero":0, "ra":1, "sp":2, "gp":3, "tp":4,
    "t0":5, "t1":6, "t2":7,
    "s0":8, "s1":9,
    "a0":10, "a1":11, "a2":12, "a3":13,
    "a4":14, "a5":15, "a6":16, "a7":17,
    "s2":18, "s3":19, "s4":20, "s5":21,
    "s6":22, "s7":23, "s8":24, "s9":25,
    "s10":26, "s11":27,
    "t3":28, "t4":29, "t5":30, "t6":31
}

def j_type(PC, rd_name, offset):
    opcode = "1101111"
    rd = format(reg_map[rd_name], "05b")

    imm21 = offset
    if(imm21 < 0):
        imm21 = (1 << 21) + imm21

    imm_bits = format(imm21, "021b")  

    imm20     = imm_bits[0]
    imm10_1   = imm_bits[10:20]   
    imm11     = imm_bits[9]       
    imm19_12  = imm_bits[1:9]    

    imm_encoded = imm20 + imm10_1 + imm11 + imm19_12  

    return imm_encoded + rd + opcode