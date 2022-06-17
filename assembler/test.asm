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

CLK_MODE = 0x00
IRQ_SRC = 0x01
IRQ_MASK = 0x02
DMA_DST_BR = 0x03
DMA_DST_HI = 0x04
DMA_DST_LO = 0x05
DMA_SRC_BR = 0x06
DMA_SRC_HI = 0x07
DMA_SRC_LO = 0x08
DMA_LEN_HI = 0x09
DMA_LEN_LO = 0x0A
UART_RX = 0x0B
UART_TX = 0x0C
UART_CTRL = 0x0D

#addr 0
jmp.abs rst
#addr 3
jmp.abs irq


irq:
    halt

rst:
    out <UART_TX>, #69
    out <UART_TX>, #42
    out <UART_TX>, #80
    out <UART_TX>, #08
