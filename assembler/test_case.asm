#include "bw8cpu.asm"

#ruledef testing_opcodes {
    musteq a, #{imm: i8} => opcode(OP_MUSTEQ_A_IMM) @ imm
    musteq b, #{imm: i8} => opcode(OP_MUSTEQ_B_IMM) @ imm
    musteq c, #{imm: i8} => opcode(OP_MUSTEQ_C_IMM) @ imm
    musteq d, #{imm: i8} => opcode(OP_MUSTEQ_D_IMM) @ imm
}

jmp.abs rst

irq:
    inc a
    rti

rst:
    load a, #0b00100001
    push a

    load x, #.loop
    push x

    rti

    .loop:
        jmp .loop