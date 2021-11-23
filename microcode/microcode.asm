#include "ctrl_lines.asm"
#include "ctrl_state.asm"
#bits 32

_fetch = ADDR_ASSERT_PC | DBUS_ASSERT_MEM | DBUS_LOAD_IR | COUNT_INC_PC

#ruledef {
    fetch              => _fetch`32
    uop {value}        => value`32

    final              => RST_USEQ`32
    final_brk          => RST_BRK_CLK`32
    final_ext1         => RST_USEQ_EXT1`32
    final_ext2         => RST_USEQ_EXT2`32

    final {value}      => (value | RST_USEQ)`32
    final_ext1 {value} => (value | RST_USEQ_EXT1)`32
    final_ext2 {value} => (value | RST_USEQ_EXT2)`32
}

#ruledef {
    mov_dbus {dst} {src} => asm {
        fetch
        final (dst << 4) | (src << 0) 
    }
}

#bank mode00
nop:
    fetch
    final

#align 8 * 32
break:
    fetch
    final_brk

#align 8 * 32
ext1:
    fetch
    final_ext1

#align 8 * 32
ext2:
    fetch
    final_ext2

#align 8 * 32
clc:
    fetch
    final ALU_CLC

#align 8 * 32
cli:
    fetch
    final ALU_CLI

#align 8 * 32
clv:
    fetch
    final ALU_CLV

#align 8 * 32
sec:
    fetch
    final ALU_SEC

#align 8 * 32
sei:
    fetch
    final ALU_SEI

#align 8 * 32
mov_a_b:
    fetch
    final DBUS_LOAD_A | DBUS_ASSERT_B

#align 8 * 32
mov_a_c:
    fetch
    final DBUS_LOAD_A | DBUS_ASSERT_C


#align 8 * 32
mov_dbus A_DBUS C_DBUS

#bank mode01
#bank mode10
#bank mode11
#bank irq