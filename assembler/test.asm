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

load x, #0x6809
mov y, x
mov sp, x