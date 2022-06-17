#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

#ruledef testing_opcodes {
    musteq a, #{imm: i8} => opcode(OP_MUSTEQ_A_IMM) @ imm
    musteq b, #{imm: i8} => opcode(OP_MUSTEQ_B_IMM) @ imm
    musteq c, #{imm: i8} => opcode(OP_MUSTEQ_C_IMM) @ imm
    musteq d, #{imm: i8} => opcode(OP_MUSTEQ_D_IMM) @ imm
}

load x, #0xFFFF
dec x