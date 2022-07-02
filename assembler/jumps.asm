#include "bw8cpu.asm"

UART_TX = 0x0C

load a, #0
load b, #0
loop:
    cmp a, b
    jo .jump
    .no_jump:
        out <UART_TX>, #"."
        jmp .post_jump
    .jump:
        out <UART_TX>, #"#"
    .post_jump:
        inc b
        cmp b, #0
        je ..inc_a
        jmp loop
        ..inc_a:
            out <UART_TX>, #"\n"
            inc a
            cmp a, #0
            jne loop
            halt
