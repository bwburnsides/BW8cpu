#include "ctrl_state.asm"
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
    ; Software Interrupt
    ; Perform the interrupt sequence, using the address in src as the ISR Vector
    swi {src: reg16} => {
        assert(src == X_XFER || src == Y_XFER)
        asm {
            fetch
            uop COUNT_DEC_SP                                                                                ;  decrement SP to prepare for push
            uop ADDR_ASSERT_SP | DBUS_ASSERT_SR | DBUS_LOAD_MEM | COUNT_DEC_SP                              ;  push flags to stack
            uop ADDR_ASSERT_SP | XFER_ASSERT_PC | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_MEM | COUNT_DEC_SP  ;  push PC-lo to stack
            uop ADDR_ASSERT_SP | XFER_ASSERT_PC | ALU_LHS | DBUS_ASSERT_ALU | DBUS_LOAD_MEM                 ;  push PC-hi to stack
            uop (src << ADDR_ASSERT) | (src << COUNT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | ALU_SEI            ;  disable interrupts and read ISR-hi
            uop (src << ADDR_ASSERT) | ((src + 3) << COUNT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1                ;  read ISR-lo and reset Y value
            final XFER_ASSERT_T | XFER_LOAD_PC                                                              ;  move ISR to PC
        }
    }

    ; Move (8-bit)
    ; Move the contents of one 8-bit register to another
    mov {dst: reg8} {src: reg8} => {
        assert(dst != src)
        asm {
            fetch
            final (dst << DBUS_LOAD) | (src << DBUS_ASSERT)
        }
    }

    ; Move (16-bit)
    ; Move the contents of one 16-bit register to another
    mov {dst: reg16} {src: reg16} => {
        assert(dst != src)
        asm {
            fetch
            final (dst << XFER_LOAD) | (src << XFER_ASSERT)
        }
    }

    ; Load Immediate (8-bit)
    ; Load 8-bit register with 8-bit constant from inst stream
    load_imm {dst: reg8} => {
        asm {
            fetch
            final READ_PC | (dst << DBUS_LOAD)
        }
    }

    ; Load Immediate (16-bit)
    ; Load 16-bit register with 16-bit constant from inst stream
    load_imm {dst: reg16} => {
        assert(dst != SP_XFER)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                  ; load imm-hi
            uop READ_PC | DBUS_LOAD_T1                  ; load imm-lo
            final XFER_ASSERT_T | (dst << XFER_LOAD)    ; move imm to dst
        }
    }

    ; Load Absolute (8-bit)
    ; Load 8-bit register with value found at absolute addr given in inst stream
    load_abs {dst: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                  ; read abs-hi
            uop READ_PC | DBUS_LOAD_T1                                  ; read abs-lo
            final ADDR_ASSERT_T | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)  ; read from abs into dst
        }
    }

    ; Load Absolute (16-bit)
    ; Load 16-bit register with value found at absolute addr and addr + 1 given in inst stream
    load_abs {dst: reg16} => {
        assert(dst != SP_XFER)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                                  ; read abs-hi
            uop READ_PC | DBUS_LOAD_T1                                                  ; read abs-lo
            uop XFER_ASSERT_T | (dst << XFER_LOAD)                                      ; move addr to dst
            uop (dst << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | (dst << COUNT)  ; read val-hi and inc ptr
            uop (dst << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1                   ; read val-lo
            final XFER_ASSERT_T | (dst << XFER_LOAD)                                    ; move val to dst
        }
    }

    ; Load Zero Page (8-bit)
    ; Load 8-bit register with value found at zeropage addr given in inst stream 
    load_zpg {dst: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1
            uop ADDR_ASSERT_DP | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)
        }
    }

    ; Load Zero Page (16-bit)
    ; Load 16-bit register with value found at zeropage addr and addr + 1 given in inst stream 
    load_zpg {dst: reg16} => {
        assert(dst != SP_XFER)
        assert(dst != E_XFER)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                                  ; read zpg addr to t-lo
            uop DBUS_ASSERT_DP | DBUS_LOAD_T2                                           ; move dp-hi to t-hi
            uop XFER_ASSERT_T | (dst << XFER_LOAD)                                      ; move t to dst
            uop (dst << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | (dst << COUNT)  ; read val-hi into t-hi
            uop (dst << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1                   ; read val-lo into t-lo
            final XFER_ASSERT_T | (dst << XFER_LOAD)                                    ; move t to dst
        }
    }

    ; Load Zero Page (16-bit, E as dst)
    ; Load 16-bit register with value found at zeropage addr and addr + 1 given in inst stream
    load_zpg {dst: reg16} => {
        assert(dst == E_XFER)
        asm {
            final  ; TODO
        }
    }

    ; Load Pointer (8-bit)
    ; Load 8-bit register with value from addr given in 16-bit register
    load_ptr {dst: reg8} {ptr: reg16} => {
        assert(ptr != SP_XFER)
        asm {
            fetch
            final (ptr << ADDR_ASSERT) | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)
        }
    }

    ; Load Pointer (16-bit)
    ; Load 16-bit register with value from addr given in index register
    load_ptr {dst: reg16} {ptr: reg16} => {
        assert (ptr == X_XFER || ptr == Y_XFER)
        asm {
            fetch
            uop (ptr << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | (ptr << COUNT)          ; read val-hi and inc ptr
            uop (ptr << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1 | ((ptr + 3) << COUNT)    ; read val-lo and dec ptr to preserve
            final XFER_ASSERT_T | (dst << XFER_LOAD)                                            ; move val to dst
        }
    }

    ; Load Pointer (16-bit, E as ptr)
    ; Load 16-bit register with value from addr given in E Accumulator
    load_ptr {dst: reg16} {ptr: reg16} => {
        assert(ptr == E_XFER)
        asm {
            fetch
            uop DBUS_ASSERT_A | DBUS_LOAD_T2                    ; move E-hi to T-hi
            uop DBUS_ASSERT_B | DBUS_LOAD_T1                    ; move E-lo to T-lo
            uop COUNT_INC_T                                     ; inc T - now E points to val-hi and T points to val-lo
            uop ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_T1  ; read val-lo to t-lo
            uop ADDR_ASSERT_E | DBUS_ASSERT_MEM | DBUS_LOAD_T2  ; read val-hi to t-hi
            final XFER_ASSERT_T | (dst << XFER_LOAD)            ; move val to dst
        }
    }

    ; TODO: Figure out how to handle the XFER 8-bit asserts with bitwise operations
    ; load_const_idx {dst: reg8} {ptr: reg16} => {
    ;     asm {
    ;         fetch
    ;         uop READ_PC | (dst << DBUS_LOAD)  ; read offset into dst
    ;         uop (ptr << XFER_ASSERT) | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move ptr-Lo into T1
    ;         uop XFER_ASSERT_A_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and X-Lo into T1
    ;         uop XFER_ASSERT_X | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add X-Hi and Cf into T2
    ;         final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
    ;     }
    ; }

    ; Store Zero Page (8-bit)
    ; Store the contents of an 8-bit register to the zeropage addr given in inst stream
    store_zpg {src: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1
            final ADDR_ASSERT_DP | DBUS_LOAD_MEM | (src << DBUS_ASSERT)
        }
    }

    ; Store Zero Page (16-bit)
    ; Store the contents of a 16-bit register to the zeropage addr and addr+1 given in inst stream
    store_zpg {src: reg16} => {
        assert(src != SP_XFER)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1
            uop (src << XFER_ASSERT) | ALU_LHS | DBUS_ASSERT_ALU | ADDR_ASSERT_DP | DBUS_LOAD_MEM | COUNT_INC_T
            final (src << XFER_ASSERT) | ALU_RHS | DBUS_ASSERT_ALU | ADDR_ASSERT_DP | DBUS_LOAD_MEM
        }
    }

    store_abs {src: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2
            uop READ_PC | DBUS_LOAD_T1
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (src << DBUS_ASSERT)
        }
    }

    store_abs {src: reg16} => {
        assert(src != SP_XFER)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2
            uop READ_PC | DBUS_LOAD_T1
            uop ADDR_ASSERT_T | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_LHS | DBUS_ASSERT_ALU | COUNT_INC_T
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_RHS | DBUS_ASSERT_ALU
        }
    }

    store_ptr {src: reg8} {ptr: reg16} => {
        assert(ptr != SP_XFER)
        asm {
            fetch
            final (ptr << ADDR_ASSERT) | DBUS_LOAD_MEM | (src << DBUS_ASSERT)
        }
    }

    push {src: reg8} => {
        asm {
            fetch
            uop COUNT_DEC_SP
            final ADDR_ASSERT_SP | DBUS_LOAD_MEM | (src << DBUS_ASSERT)
        }
    }

    push {src: reg16} => {
        assert(src != SP_XFER)
        asm {
            fetch
            uop COUNT_DEC_SP
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_LHS | DBUS_ASSERT_ALU | COUNT_DEC_SP
            final ADDR_ASSERT_SP | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_RHS | DBUS_ASSERT_ALU
        }
    }

    pop {dst: reg8} => {
        asm {
            fetch
            final ADDR_ASSERT_SP | DBUS_ASSERT_MEM | (dst << DBUS_LOAD) | COUNT_INC_SP
        }
    }

    pop {dst: reg16} => {
        assert(dst != SP_XFER)
        asm {
            fetch
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | COUNT_INC_SP
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T1
            final (dst << XFER_LOAD) | XFER_ASSERT_T
        }
    }
}