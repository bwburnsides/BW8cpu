#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

load x, #0xFFFF
mov sp, x
load x, #0x0000
top:
    load a, #0xFF
    load b, #0xFF
    load c, #0xFF
    load d, #0xFF
    jsr set_registers
    load a, #0x00
    load b, #0x00
    load c, #0x00
    load d, #0x00

    jmp top


set_registers:
    load x, #0xFFFF
    load y, #0xFFFF
    rts
