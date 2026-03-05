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

def u_type(instruct, register, num):
    opcode = {"lui": "0110111", "auipc": "0010111"}

    # If number is negative then taking 2's compliment of it
    if(num < 0):
        num = (1 << 20) + num

    binary_num = format(num, "020b")       # Converting into 20 bits binary number
    binary_reg = format(reg_map[register], "05b")        # Converting into 5 bits binary number
    return binary_num + binary_reg + opcode[instruct]