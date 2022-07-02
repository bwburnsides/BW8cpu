#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

#noemit on
CLK_BASE = 0x00
CLK_MODE = CLK_BASE | 0x0

IRQ_BASE = 0x10
IRQ_SRC = IRQ_BASE | 0x0
IRQ_MASK = IRQ_BASE | 0x1

DMA_BASE = 0x20
DMA_DST_BR = DMA_BASE | 0x0
DMA_DST_HI = DMA_BASE | 0x1
DMA_DST_LO = DMA_BASE | 0x2
DMA_SRC_BR = DMA_BASE | 0x3
DMA_SRC_HI = DMA_BASE | 0x4
DMA_SRC_LO = DMA_BASE | 0x5
DMA_LEN_HI = DMA_BASE | 0x6
DMA_LEN_LO = DMA_BASE | 0x7

UART_BASE = 0x30
UART_RX = UART_BASE | 0x0
UART_TX = UART_BASE | 0x1
UART_CTRL = UART_BASE | 0x2
#noemit off
; --------------------------------

load a, #0
load b, #1
cmp a, b
jle .jump
.no_jump:
    out <UART_TX>, #"."
    halt
.jump:
    out <UART_TX>, #"#"
    halt
