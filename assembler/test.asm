#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

nop
clc
nop
