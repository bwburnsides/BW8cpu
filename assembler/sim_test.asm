#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0x8000
    #outp 0
    #fill
}

#bankdef ram {
    #addr 0x8000
    #size 0x8000
}

#ruledef testing_opcodes {
    musteq a, #{imm: i8} => opcode(OP_MUSTEQ_A_IMM) @ imm
    musteq b, #{imm: i8} => opcode(OP_MUSTEQ_B_IMM) @ imm
    musteq c, #{imm: i8} => opcode(OP_MUSTEQ_C_IMM) @ imm
    musteq d, #{imm: i8} => opcode(OP_MUSTEQ_D_IMM) @ imm
}

#bank rom

jmp.abs rst
jmp.abs irq
jmp.abs nmi

nmi:
    inc d
    rti

irq:
    inc c
    rti

rst:
    load a, #0b00100001
    push a
    load x, #usr
    push x
    load a, #0
    load x, #0
    rti

usr:
    load a, #direct_page[15:8]
    mov dp, a

    load a, #4
    ; store [0x8000], a
    store [!4], a

    ; clc
    ; adc [!0], #3

    ; load b, [!0]

#bank ram
#addr 0x8000

direct_page:
    #res 256