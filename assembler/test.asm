#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

load a, #0x69
load b, #0x70
load c, #0x71
load d, #0x72
