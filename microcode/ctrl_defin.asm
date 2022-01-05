#include "ctrl_lines.asm"

READ_PC = ADDR_ASSERT_PC | COUNT_INC_PC | DBUS_ASSERT_MEM
_fetch = READ_PC | DBUS_LOAD_IR

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

#subruledef reg8 {
    a => A_DBUS
    b => B_DBUS
    c => C_DBUS
    d => D_DBUS
}

#subruledef reg16 {
    sp => SP_XFER
    e  => E_XFER
    x  => X_XFER
    y  => Y_XFER
}

#ruledef {
    ; MOV (8-bit version)
    mov {dst: reg8} {src: reg8} => {
        assert(dst != src)
        asm {
            fetch
            final (dst << DBUS_LOAD) | (src << DBUS_ASSERT) 
        }
    }

    ; MOV (16-bit version)
    mov {dst: reg16} {src: reg16} => {
        assert(dst != src)
        asm {
            fetch
            final (dst << XFER_LOAD) | (src << XFER_ASSERT)
        }
    }

    ; Load 8-bit register with immediate value
    load_imm {dst: reg8} => {
        asm {
            fetch
            final READ_PC | (dst << DBUS_LOAD)
        }
    }

    ; Load 8-bit register from absolute address
    load_abs {dst: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2
            uop READ_PC | DBUS_LOAD_T1
            uop ADDR_ASSERT_T | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)
        }
    }

    ; Load 8-bit register from zeropage address 
    load_zpg {dst: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1
            uop ADDR_ASSERT_DP | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)
        }
    }

    load_ptr {dst: reg8} {src: reg16} => {
        asm {
            fetch
            final (src << ADDR_ASSERT) | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)
        }
    }

    load_const_idx {dst: reg8} {src: }
}