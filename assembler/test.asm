; #include "bw8cpu.asm"
#include "minimalbw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

load a, #"U"
mov dp, a
mov b, a

load a, #"F"
load c, #"C"
load d, #"K"

brk

load a, #255
load b, #1

brk

adc a, b
clc

brk

load a, #0b1010_1010
load b, #0b0101_0101

brk

and a, b

brk
