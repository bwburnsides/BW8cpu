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

#bank rom

itoa:
    push c
    push x

    load x, #.hex_table

    mov c, a
    and a, #0xF
    load b, [x, a]

    clc
    src c
    src c
    src c
    src c
    mov a, c
    and a, #0xF
    load a, [x, a]

    pop x
    pop c
    rts

    .hex_table:
        #d "0123456789ABCDEF"