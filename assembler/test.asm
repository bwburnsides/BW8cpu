#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

#ruledef emulator {
    halt => opcode(OP_EXT) @ 0xFC
}

rst:
    load a, #0xFF
    load b, #0x01

    adc a, b

    jnz not_zero
    jz zero

#addr 0x8000
not_zero:
    halt

#addr 0x9000
zero:
    halt