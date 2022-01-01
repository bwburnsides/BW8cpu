#include "ctrl_lines.asm"
#include ""

#subruledef gpr8 {
    a => A_DBUS
    b => B_DBUS
    c => C_DBUS
    d => D_DBUS
}

#ruledef {
    mov {dst: gpr8} {src: gpr8} => 0x01 @ dst`8 @ src`8
}