#include "ctrl_state.asm"
#include "ctrl_defin.asm"

#bits 32
#labelalign 8 * 32

#bank mode00
nop:
    fetch
    final
break:
    fetch
    final_brk
ext1:
    fetch
    final_ext1
ext2:
    fetch
    final_ext2
clc:
    fetch
    final ALU_CLC
cli:
    fetch
    final ALU_CLI
clv:
    fetch
    final ALU_CLV
sec:
    fetch
    final ALU_SEC
sei:
    fetch
    final ALU_SEI

mov a b
mov a c
mov a d

mov b a
mov b c
mov b d

mov c a
mov c b
mov c d

mov d a
mov d b
mov d c

mov sp x
mov sp y
mov sp e

mov x y
mov x e
mov x sp

mov y x
mov y e
mov y sp

mov e x
mov e y
mov e sp


#bank mode01
#bank mode10
#bank mode11
#bank irq