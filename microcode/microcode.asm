; #include "ctrl_lines.asm"
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

mov_dbus A_DBUS B_DBUS
mov_dbus A_DBUS C_DBUS
mov_dbus A_DBUS D_DBUS
mov_dbus A_DBUS DP_DBUS
mov_dbus B_DBUS A_DBUS
mov_dbus B_DBUS C_DBUS
mov_dbus B_DBUS D_DBUS
mov_dbus B_DBUS DP_DBUS
mov_dbus C_DBUS A_DBUS
mov_dbus C_DBUS B_DBUS
mov_dbus C_DBUS D_DBUS
mov_dbus C_DBUS DP_DBUS
mov_dbus D_DBUS A_DBUS
mov_dbus D_DBUS B_DBUS
mov_dbus D_DBUS C_DBUS
mov_dbus D_DBUS DP_DBUS
mov_dbus DP_DBUS A_DBUS
mov_dbus DP_DBUS B_DBUS
mov_dbus DP_DBUS C_DBUS
mov_dbus DP_DBUS D_DBUS

mov_xfer SP_XFER X_XFER
mov_xfer SP_XFER Y_XFER
mov_xfer SP_XFER E_XFER
mov_xfer X_XFER Y_XFER
mov_xfer X_XFER E_XFER
mov_xfer X_XFER SP_XFER
mov_xfer Y_XFER X_XFER
mov_xfer Y_XFER E_XFER
mov_xfer Y_XFER SP_XFER
mov_xfer E_XFER X_XFER
mov_xfer E_XFER Y_XFER
mov_xfer E_XFER SP_XFER


#bank mode01
#bank mode10
#bank mode11
#bank irq