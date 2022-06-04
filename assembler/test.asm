#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

load x, #0x6809
load a, #255
load b, #1
adc a, b
jmp_abs 0x000