#include "ctrl_state.asm"
#include "ctrl_lines.asm"

READ_PC = ADDR_ASSERT_PC | COUNT_INC_PC | DBUS_ASSERT_MEM
_fetch = READ_PC | DBUS_LOAD_IR

#ruledef {
    fetch              => _fetch`32
    uop {value}        => value`32
    final              => RST_USEQ`32
    final {value}      => (value | RST_USEQ)`32
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

#subruledef regidx {
    x => X_XFER
    y => Y_XFER
}

#subruledef xfer_assert_reg8_t1 {
    a => A_DBUS`4 @ XFER_ASSERT_A_T1`5
    b => B_DBUS`4 @ XFER_ASSERT_B_T1`5
    c => C_DBUS`4 @ XFER_ASSERT_C_T1`5
    d => D_DBUS`4 @ XFER_ASSERT_D_T1`5
}

#subruledef xfer_assert_acc8_t1 {
    a => XFER_ASSERT_A_T1
    b => XFER_ASSERT_B_T1
}

#ruledef {
    ; Software Interrupt
    ; Perform the interrupt sequence, using the address in src as the ISR Vector
    swi {src: regidx} => {
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
        assert(dst != src)  ; inst doesn't support same src as dst
        asm {
            fetch
            final (dst << DBUS_LOAD) | (src << DBUS_ASSERT)  ; move src to dst via dbus
        }
    }

    ; Move (16-bit)
    ; Move the contents of one 16-bit register to another
    mov {dst: reg16} {src: reg16} => {
        assert(dst != src)  ; inst doesn't support same src as dst
        asm {
            fetch
            final (dst << XFER_LOAD) | (src << XFER_ASSERT)  ; move src to dst via dbus
        }
    }

    ; Load Immediate (8-bit)
    ; Load 8-bit register with 8-bit constant from inst stream
    load_imm {dst: reg8} => {
        asm {
            fetch
            final READ_PC | (dst << DBUS_LOAD)  ; read inst stream into dst via dbus
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
            uop READ_PC | DBUS_LOAD_T1                                  ; read zpg addr into t1 / dp
            uop ADDR_ASSERT_DP | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)   ; read from dp into dst
        }
    }

    ; Load Zero Page (16-bit)
    ; Load 16-bit register with value found at zeropage addr and addr + 1 given in inst stream 
    load_zpg {dst: regidx} => {
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
            fetch
            uop READ_PC | DBUS_LOAD_T1                                          ; read zpg addr to t1 / dp
            uop ADDR_ASSERT_DP | DBUS_ASSERT_MEM | DBUS_LOAD_A | COUNT_INC_T    ; read from dp into A (E-hi)
            final ADDR_ASSERT_DP | DBUS_ASSERT_MEM | DBUS_LOAD_B                ; read from dp into B (E-lo)
        }
    }

    ; Load Pointer (8-bit)
    ; Load 8-bit register with value from addr given in 16-bit register
    load_ptr {dst: reg8} {ptr: reg16} => {
        assert(ptr != SP_XFER)
        asm {
            fetch
            final (ptr << ADDR_ASSERT) | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)  ; read from ptr into dst
        }
    }

    ; Load Pointer (16-bit)
    ; Load 16-bit register with value from addr given in index register
    load_ptr {dst: reg16} {ptr: regidx} => {
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

    ; Load Pointer with Constant Offset (8-bit)
    ; Load 8-bit register with value from addr given by value
    ; in 16-bit register + constant offset given in inst stream
    load_const_idx {dst: xfer_assert_reg8_t1} {ptr: reg16} => {
        asm {
            fetch
            uop READ_PC | (dst[3:0] << DBUS_LOAD)                                       ; read offset into dst
            uop (ptr << XFER_ASSERT) | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1         ; move ptr-Lo into T1
            uop (dst[8:4] << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1    ; add offset and X-Lo into T1
            uop XFER_ASSERT_X | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2              ; add X-Hi and Cf into T2
            final ADDR_ASSERT_T | DBUS_ASSERT_MEM | (dst[3:0] << DBUS_LOAD)             ; read from temp into A
        }
    }

    ; Load Pointer with Accumulator Offset (8-bit)
    ; Load 8-bit register with value from addr given by value
    ; in 16-bit register + offset given in an accumulator
    load_acc_idx {dst: reg8} {acc: xfer_assert_acc8_t1} {ptr: reg16} => {
        assert(ptr != E_XFER)
        asm {
            fetch
            uop (ptr << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | DBUS_LOAD_T1     ; move ptr-lo to t-lo
            uop (acc << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1     ; add acc and t-lo into t-lo 
            uop (ptr << XFER_ASSERT) | ALU_MSB_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2   ; add ptr-hi and Cf into t-hi
            uop ADDR_ASSERT_T | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)                ; read from t into dst
        }
    }

    ; Load Zero Page with Accumulator Offset (8-bit)
    ; Load 8-bit register with value given by zero page addr incremented by
    ; accumulator value
    load_acc_zpg {dst: reg8} {acc: xfer_assert_acc8_t1} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                              ; read zpg addr into t1
            uop (acc << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1     ; add t-lo and acc into t-lo
            final ADDR_ASSERT_DP | DBUS_ASSERT_MEM | (dst << DBUS_LOAD)             ; read from addr into dst
        }
    }

    ; Store Zero Page (8-bit)
    ; Store the contents of an 8-bit register to the zeropage addr given in inst stream
    store_zpg {src: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                      ; read zpg addr into t1/dp
            final ADDR_ASSERT_DP | DBUS_LOAD_MEM | (src << DBUS_ASSERT)     ; write src to dp addr
        }
    }

    ; Store Zero Page (16-bit)
    ; Store the contents of a 16-bit register to the zeropage addr and addr+1 given in inst stream
    store_zpg {src: reg16} => {
        assert(src != SP_XFER)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                                                              ; read zpg addr into t1/dp
            uop (src << XFER_ASSERT) | ALU_MSB | DBUS_ASSERT_ALU | ADDR_ASSERT_DP | DBUS_LOAD_MEM | COUNT_INC_T     ; write src-hi to dp
            final (src << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | ADDR_ASSERT_DP | DBUS_LOAD_MEM                 ; write src-lo to dp+1
        }
    }

    ; Store Absolute (8-bit)
    ; Store the contents of an 8-bit register to the absolute addr given in inst stream
    store_abs {src: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                  ; read abs-hi into t-hi
            uop READ_PC | DBUS_LOAD_T1                                  ; read abs-lo into t-lo
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (src << DBUS_ASSERT)  ; write src to t addr
        }
    }

    ; Store Absolute (16-bit)
    ; Store the contents of a 16-bit register to the absolute addr and addr+1 given in inst stream
    store_abs {src: reg16} => {
        assert(src != SP_XFER)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                                                          ; read abs-hi into t-hi
            uop READ_PC | DBUS_LOAD_T1                                                                          ; read abs-lo into t-lo
            uop ADDR_ASSERT_T | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_MSB | DBUS_ASSERT_ALU | COUNT_INC_T  ; write src-hi to addr
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU              ; write src-lo to addr+1
        }
    }

    ; Store Pointer (8-bit)
    ; Store the contents of an 8-bit register to the addr given in a 16-bit register
    store_ptr {src: reg8} {ptr: reg16} => {
        assert(ptr != SP_XFER)
        asm {
            fetch
            final (ptr << ADDR_ASSERT) | DBUS_LOAD_MEM | (src << DBUS_ASSERT)  ; write src to ptr addr
        }
    }

    ; Push (8-bit)
    ; Store the contents of an 8-bit register to the top of the stack
    push {src: reg8} => {
        asm {
            fetch
            uop COUNT_DEC_SP                                                ; dec SP to prep for push
            final ADDR_ASSERT_SP | DBUS_LOAD_MEM | (src << DBUS_ASSERT)     ; write src to sp
        }
    }

    ; Push (16-bit)
    ; Store the contents of a 16-bit register to the top of the stack
    push {src: reg16} => {
        assert(src != SP_XFER)
        asm {
            fetch
            uop COUNT_DEC_SP                                                                                        ; dec sp to prep for push
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | COUNT_DEC_SP    ; write src-lo to sp
            final ADDR_ASSERT_SP | DBUS_LOAD_MEM | (src << XFER_ASSERT) | ALU_MSB | DBUS_ASSERT_ALU                 ; write src-hi to sp-1
        }
    }

    ; Pop (8-bit)
    ; Load an 8-bit register with the contents at the top of the stack
    pop {dst: reg8} => {
        asm {
            fetch
            final ADDR_ASSERT_SP | DBUS_ASSERT_MEM | (dst << DBUS_LOAD) | COUNT_INC_SP  ; read from SP into dst
        }
    }

    ; Pop (16-bit)
    ; Load a 16-bit register with the contents at the top of the stack
    pop {dst: reg16} => {
        assert(dst != SP_XFER)
        asm {
            fetch
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | COUNT_INC_SP  ; read hi into t-hi
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T1                 ; read lo into t-lo
            final (dst << XFER_LOAD) | XFER_ASSERT_T                            ; move t to dst
        }
    }
}