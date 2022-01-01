#include "ctrl_lines.asm"

_fetch = ADDR_ASSERT_PC | DBUS_ASSERT_MEM | DBUS_LOAD_IR | COUNT_INC_PC

#ruledef {
    fetch              => _fetch`32
    uop {value}        => value`32
    zero               => 0`32

    final              => RST_USEQ`32
    final_brk          => (RST_USEQ | BRK_CLK)`32
    final_ext1         => (RST_USEQ | TOG_EXT1)`32
    final_ext2         => (RST_USEQ | TOG_EXT2)`32

    final {value}      => (value | RST_USEQ)`32
    final_ext1 {value} => (value | RST_USEQ | TOG_EXT1)`32
    final_ext2 {value} => (value | RST_USEQ | TOG_EXT2)`32
}

#ruledef {
    mov_dbus {dst} {src} => asm {
        fetch
        final (dst << DBUS_LOAD) | (src << DBUS_ASSERT) 
        zero
        zero
        zero
        zero
        zero
        zero
    }

    mov_xfer {dst} {src} => asm {
        fetch
        final (dst << XFER_LOAD) | (src << XFER_ASSERT)
        zero
        zero
        zero
        zero
        zero
        zero
    }
}