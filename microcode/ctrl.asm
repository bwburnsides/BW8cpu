#once
#include "ctrl_state.asm"
#include "ctrl_lines.asm"

#bits 32
#labelalign 8 * 32  ; TODO: talk to developer - this doesnt seem to function as intended

READ_PC = ADDR_ASSERT_PC | COUNT_INC_PC | DBUS_ASSERT_MEM
_fetch = READ_PC | DBUS_LOAD_IR

_A  = (XFER_ASSERT_A_A >> XFER_ASSERT)`5 @ (XFER_ASSERT_A_T1 >> XFER_ASSERT)`5 @ (XFER_ASSERT_T2_A >> XFER_ASSERT)`5 @ A_DBUS`4
_B  = (XFER_ASSERT_B_B >> XFER_ASSERT)`5 @ (XFER_ASSERT_B_T1 >> XFER_ASSERT)`5 @ (XFER_ASSERT_T2_B >> XFER_ASSERT)`5 @ B_DBUS`4
_C  = (XFER_ASSERT_C_C >> XFER_ASSERT)`5 @ (XFER_ASSERT_C_T1 >> XFER_ASSERT)`5 @ (XFER_ASSERT_T2_C >> XFER_ASSERT)`5 @ C_DBUS`4
_D  = (XFER_ASSERT_D_D >> XFER_ASSERT)`5 @ (XFER_ASSERT_D_T1 >> XFER_ASSERT)`5 @ (XFER_ASSERT_T2_D >> XFER_ASSERT)`5 @ D_DBUS`4
_E  = E_XFER`3
_X  = (COUNT_INC_X  >> COUNT)`3 @  X_XFER`3 
_Y  = (COUNT_INC_Y  >> COUNT)`3 @  Y_XFER`3 
_SP = (COUNT_INC_SP >> COUNT)`3 @ SP_XFER`3

#fn id8(val)        => val[3:0]
#fn xa_t2_r8(val)   => val[8:4]
#fn xa_r8_t1(val)   => val[13:9]
#fn xa_r8_r8(val)   => val[18:14]

#fn id16(val)       => val[2:0]
#fn inc(val)        => val[5:3]
DEC_OFFSET          = 3

#ruledef {
    fetch           => _fetch`32
    uop {value}     => value`32
    final           => RST_USEQ`32
    final {value}   => (value | RST_USEQ)`32
}

#ruledef {
    zero {val} => {
        assert(val == 1)
        0`32
    }
    zero {val} => {
        assert(val == 2)
        0`64
    }
    zero {val} => {
        assert(val == 3)
        0`96
    }
    zero {val} => {
        assert(val == 4)
        0`128
    }
    zero {val} => {
        assert(val == 5)
        0`160
    }
    zero {val} => {
        assert(val == 6)
        0`192
    }
    zero {val} => {
        assert(val == 7)
        0`224
    }
}

#subruledef reg8 {
    a => _A 
    b => _B
    c => _C
    d => _D
}

#subruledef acc8 {
    a => _A
    b => _B
}

#subruledef reg16 {
    sp => _SP
    e  => _E
    x  => _X
    y  => _Y
}

#subruledef idx16 {
    x => _X
    y => _Y
}

#subruledef acc16 {
    e => _E
}

#ruledef Housekeeping {
    ; No Operation
    ; Do nothing and then move on
    nop => {
        asm {
            fetch
            final
            zero 6
        }
    }

    ; Break
    ; Put the clock into single-step mode
    brk => {
        asm {
            fetch
            final BRK_CLK
            zero 6
        }
    }

    ; Software Interrupt
    ; Perform the interrupt sequence, using the address in src as the ISR Vector
    swi {src: idx16} => {
        asm {
            fetch
            uop COUNT_DEC_SP                                                                                        ;  decrement SP to prepare for push
            uop ADDR_ASSERT_SP | DBUS_ASSERT_SR | DBUS_LOAD_MEM | COUNT_DEC_SP                                      ;  push flags to stack
            uop ADDR_ASSERT_SP | XFER_ASSERT_PC | ALU_LSB | DBUS_ASSERT_ALU | DBUS_LOAD_MEM | COUNT_DEC_SP          ;  push PC-lo to stack
            uop ADDR_ASSERT_SP | XFER_ASSERT_PC | ALU_MSB | DBUS_ASSERT_ALU | DBUS_LOAD_MEM                         ;  push PC-hi to stack
            uop (id16(src) << ADDR_ASSERT) | (inc(src) << COUNT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | ALU_SEI         ;  disable interrupts and read ISR-hi
            uop (id16(src) << ADDR_ASSERT) | ((inc(src) + DEC_OFFSET) << COUNT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1    ;  read ISR-lo and reset Y value
            final XFER_ASSERT_T | XFER_LOAD_PC                                                                      ;  move ISR to PC
        }
    }

    ; Move (8-bit)
    ; Move the contents of one 8-bit register to another
    mov {dst: reg8} {src: reg8} => {
        assert(dst != src)  ; inst doesn't support same src as dst
        asm {
            fetch
            final (id8(dst) << DBUS_LOAD) | (id8(src) << DBUS_ASSERT)   ; move src to dst via dbus
            zero 6
        }
    }

    ; Move (16-bit)
    ; Move the contents of one 16-bit register to another
    mov {dst: reg16} {src: reg16} => {
        assert(dst != src)  ; inst doesn't support same src as dst
        asm {
            fetch
            final (id16(dst) << XFER_LOAD) | (id16(src) << XFER_ASSERT)     ; move src to dst via dbus
            zero 6
        }
    }
}

#ruledef Loads {
    ; Load Immediate (8-bit)
    ; Load 8-bit register with 8-bit constant from inst stream
    load_imm {dst: reg8} => {
        asm {
            fetch
            final READ_PC | (id8(dst) << DBUS_LOAD)     ; read inst stream into dst via dbus
            zero 6
        }
    }

    ; Load Immediate (16-bit)
    ; Load 16-bit register with 16-bit constant from inst stream
    load_imm {dst: reg16} => {
        assert(dst != _SP)  ; inst doesn't support sp as dst
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                      ; load imm-hi
            uop READ_PC | DBUS_LOAD_T1                      ; load imm-lo
            final XFER_ASSERT_T | (id16(dst) << XFER_LOAD)  ; move imm to dst
            zero 4
        }
    }

    ; Load Absolute (8-bit)
    ; Load 8-bit register with value found at absolute addr given in inst stream
    load_abs {dst: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                          ; read abs-hi
            uop READ_PC | DBUS_LOAD_T1                                          ; read abs-lo
            final ADDR_ASSERT_T | DBUS_ASSERT_MEM | (id8(dst) << DBUS_LOAD)     ; read from abs into dst
            zero 4
        }
    }

    ; Load Absolute (16-bit)
    ; Load 16-bit register with value found at absolute addr and addr + 1 given in inst stream
    load_abs {dst: reg16} => {
        assert(dst != _SP)  ; inst doesn't support sp as dst
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                                              ; read abs-hi
            uop READ_PC | DBUS_LOAD_T1                                                              ; read abs-lo
            uop XFER_ASSERT_T | (dst << XFER_LOAD)                                                  ; move addr to dst
            uop (id16(dst) << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | (id16(dst) << COUNT)  ; read val-hi and inc ptr
            uop (id16(dst) << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1                         ; read val-lo
            final XFER_ASSERT_T | (id16(dst) << XFER_LOAD)                                          ; move val to dst
            zero 1
        }
    }

    ; Load Zero Page (8-bit)
    ; Load 8-bit register with value found at zeropage addr given in inst stream 
    load_zpg {dst: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                          ; read zpg addr into t1 / dp
            final ADDR_ASSERT_DP | DBUS_ASSERT_MEM | (id8(dst) << DBUS_LOAD)    ; read from dp into dst
            zero 5
        }
    }

    ; Load Zero Page (16-bit)
    ; Load 16-bit register with value found at zeropage addr and addr + 1 given in inst stream 
    load_zpg {dst: idx16} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                                              ; read zpg addr to t-lo
            uop DBUS_ASSERT_DP | DBUS_LOAD_T2                                                       ; move dp-hi to t-hi
            uop XFER_ASSERT_T | (id16(dst) << XFER_LOAD)                                            ; move t to dst
            uop (id16(dst) << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | (id16(dst) << COUNT)  ; read val-hi into t-hi
            uop (id16(dst) << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1                         ; read val-lo into t-lo
            final XFER_ASSERT_T | (id16(dst) << XFER_LOAD)                                          ; move t to dst
            zero 1
        }
    }

    ; Load Zero Page (16-bit, E as dst)
    ; Load 16-bit register with value found at zeropage addr and addr + 1 given in inst stream
    load_zpg {dst: acc16} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                          ; read zpg addr to t1 / dp
            uop ADDR_ASSERT_DP | DBUS_ASSERT_MEM | DBUS_LOAD_A | COUNT_INC_T    ; read from dp into A (E-hi)
            final ADDR_ASSERT_DP | DBUS_ASSERT_MEM | DBUS_LOAD_B                ; read from dp into B (E-lo)
            zero 4
        }
    }

    ; Load Pointer (8-bit)
    ; Load 8-bit register with value from addr given in 16-bit register
    load_ptr {dst: reg8} {ptr: reg16} => {
        assert(ptr != _SP)  ; inst doesn't support sp as ptr
        asm {
            fetch
            final (id16(ptr) << ADDR_ASSERT) | DBUS_ASSERT_MEM | (id8(dst) << DBUS_LOAD)    ; read from ptr into dst
            zero 6
        }
    }

    ; Load Pointer (16-bit)
    ; Load 16-bit register with value from addr given in index register
    load_ptr {dst: reg16} {ptr: idx16} => {
        asm {
            fetch
            uop (id16(ptr) << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | (id16(ptr) << COUNT)                  ; read val-hi and inc ptr
            uop (id16(ptr) << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T1 | ((id16(ptr) + DEC_OFFSET) << COUNT)   ; read val-lo and dec ptr to preserve
            final XFER_ASSERT_T | (id8(dst) << XFER_LOAD)                                                           ; move val to dst
            zero 4
        }
    }

    ; Load Pointer (16-bit, E as ptr)
    ; Load 16-bit register with value from addr given in E Accumulator
    load_ptr {dst: reg16} {ptr: acc16} => {
        asm {
            fetch
            uop DBUS_ASSERT_A | DBUS_LOAD_T2                    ; move E-hi to T-hi
            uop DBUS_ASSERT_B | DBUS_LOAD_T1                    ; move E-lo to T-lo
            uop COUNT_INC_T                                     ; inc T - now E points to val-hi and T points to val-lo
            uop ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_T1  ; read val-lo to t-lo
            uop ADDR_ASSERT_E | DBUS_ASSERT_MEM | DBUS_LOAD_T2  ; read val-hi to t-hi
            final XFER_ASSERT_T | (id16(dst) << XFER_LOAD)      ; move val to dst
            zero 1
        }
    }

    ; Load Pointer with Constant Offset (8-bit)
    ; Load 8-bit register with value from addr given by value
    ; in 16-bit register + constant offset given in inst stream
    load_const_idx {dst: reg8} {ptr: reg16} => {
        asm {
            fetch
            uop READ_PC | (id8(dst) << DBUS_LOAD)                                           ; read offset into dst
            uop (id16(ptr) << XFER_ASSERT) | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1       ; move ptr-Lo into T1
            uop (xa_r8_t1(dst) << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1   ; add offset and ptr-lo into T1
            uop XFER_ASSERT_X | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2                  ; add ptr-hi and Cf into T2
            final ADDR_ASSERT_T | DBUS_ASSERT_MEM | (id8(dst) << DBUS_LOAD)                 ; read from temp into dst
            zero 2
        }
    }

    ; Load Pointer with Accumulator Offset (8-bit)
    ; Load 8-bit register with value from addr given by value
    ; in 16-bit register + offset given in an accumulator
    load_acc_idx {dst: reg8} {acc: acc8} {ptr: reg16} => {
        assert(ptr != _E)
        asm {
            fetch
            uop (id16(ptr) << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | DBUS_LOAD_T1       ; move ptr-lo to t-lo
            uop (xa_r8_t1(acc) << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1   ; add acc and t-lo into t-lo 
            uop (id16(ptr) << XFER_ASSERT) | ALU_MSB_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2     ; add ptr-hi and Cf into t-hi
            final ADDR_ASSERT_T | DBUS_ASSERT_MEM | (id8(dst) << DBUS_LOAD)                 ; read from t into dst
            zero 3
        }
    }

    ; Load Zero Page with Accumulator Offset (8-bit)
    ; Load 8-bit register with value given by zero page addr incremented by
    ; accumulator value
    load_acc_zpg {dst: reg8} {acc: acc8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                                      ; read zpg addr into t1
            uop (xa_r8_t1(acc) << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1   ; add t-lo and acc into t-lo
            final ADDR_ASSERT_DP | DBUS_ASSERT_MEM | (id8(dst) << DBUS_LOAD)                ; read from addr into dst
            zero 4
        }
    }
}

#ruledef Stores {
    ; Store Zero Page (8-bit)
    ; Store the contents of an 8-bit register to the zeropage addr given in inst stream
    store_zpg {src: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                          ; read zpg addr into t1/dp
            final ADDR_ASSERT_DP | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)    ; write src to dp addr
            zero 5
        }
    }

    ; Store Zero Page (16-bit)
    ; Store the contents of a 16-bit register to the zeropage addr and addr+1 given in inst stream
    store_zpg {src: reg16} => {
        assert(src != _SP)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                                                                  ; read zpg addr into t1/dp
            uop (id16(src) << XFER_ASSERT) | ALU_MSB | DBUS_ASSERT_ALU | ADDR_ASSERT_DP | DBUS_LOAD_MEM | COUNT_INC_T   ; write src-hi to dp
            final (id16(src) << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | ADDR_ASSERT_DP | DBUS_LOAD_MEM               ; write src-lo to dp+1
            zero 4
        }
    }

    ; Store Absolute (8-bit)
    ; Store the contents of an 8-bit register to the absolute addr given in inst stream
    store_abs {src: reg8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                          ; read abs-hi into t-hi
            uop READ_PC | DBUS_LOAD_T1                                          ; read abs-lo into t-lo
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)     ; write src to t addr
            zero 4
        }
    }

    ; Store Absolute (16-bit)
    ; Store the contents of a 16-bit register to the absolute addr and addr+1 given in inst stream
    store_abs {src: reg16} => {
        assert(src != _SP)
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                                                                  ; read abs-hi into t-hi
            uop READ_PC | DBUS_LOAD_T1                                                                                  ; read abs-lo into t-lo
            uop ADDR_ASSERT_T | DBUS_LOAD_MEM | (id16(src) << XFER_ASSERT) | ALU_MSB | DBUS_ASSERT_ALU | COUNT_INC_T    ; write src-hi to addr
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (id16(src) << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU                ; write src-lo to addr+1
            zero 3
        }
    }

    ; Store Pointer (8-bit)
    ; Store the contents of an 8-bit register to the addr given in a 16-bit register
    store_ptr {src: reg8} {ptr: reg16} => {
        assert(ptr != _SP)
        asm {
            fetch
            final (id16(ptr) << ADDR_ASSERT) | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)    ; write src to ptr addr
            zero 6
        }
    }

    ; Store Pointer with Constant Offset (8-bit)
    ; Store 8-bit register value to addr given by value
    ; in 16-bit register + constant offset given in inst stream
    store_const_idx {src: reg8} {ptr: reg16} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                                      ; read offset from inst stream into t-lo
            uop (id16(ptr) << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | DBUS_LOAD_T2       ; move ptr-lo into t-hi
            uop XFER_ASSERT_T | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1                    ; add ptr-lo and t-lo into t-lo
            uop (id16(ptr) << XFER_ASSERT) | ALU_MSB_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2     ; add ptr-hi and Cf into t-hi
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)                 ; write src to dst
            zero 2
        }
    }

    ; Store Pointer with Constant Offset (8-bit, ptr=E_XFER)
    ; Store 8-bit register value to addr given by value
    ; in 16-bit register + constant offset given in inst stream
    store_const_idx {src: reg8} {ptr: acc16} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                          ; read offset from inst stream into t-lo
            uop XFER_ASSERT_B_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1     ; add E-lo (B) and t-lo into t-lo
            uop XFER_ASSERT_E | ALU_MSB_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2      ; add E-hi (A) and Cf into t-hi
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)     ; write src to T addr
            zero 3
        }
    }

    ; Store Pointer with Accumulator Offset (8-bit)
    ; Store 8-bit register value to addr given by value
    ; in 16-bit register + offset given in an accumulator
    store_acc_idx {dst: reg8} {acc: acc8} {ptr: reg16} => {
        assert(ptr != _E)  ; inst doesn't support E as ptr (TODO: include this in ISA?)
        asm {
            fetch
            uop (id16(ptr) << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | DBUS_LOAD_T1       ; move ptr-lo to 8-bit side
            uop (xa_r8_t1(acc) << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1   ; ptr-lo + acc to t-lo
            uop (id16(ptr) << XFER_ASSERT) | ALU_MSB_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2     ; ptr-hi + Cf to t-hi
            final ADDR_ASSERT_T | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)                 ; write src to T addr
            zero 3
        }
    }

    ; Store Zero Page with Accumulator Offset (8-bit)
    ; Store 8-bit register value to addr given by
    ; zero page addr incremented by accumulator value
    store_acc_zpg {src: reg8} {acc: acc8} => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                                      ; read zpg addr into t1 / dp
            uop (xa_r8_t1(acc) << XFER_ASSERT) | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1   ; add acc offset to zpg addr
            final ADDR_ASSERT_DP | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)                ; write src to DP addr
            zero 4
        }
    } 
}

#ruledef StackOperations {
    ; Push (8-bit)
    ; Store the contents of an 8-bit register to the top of the stack
    push {src: reg8} => {
        asm {
            fetch
            uop COUNT_DEC_SP                                                    ; dec SP to prep for push
            final ADDR_ASSERT_SP | DBUS_LOAD_MEM | (id8(src) << DBUS_ASSERT)    ; write src to sp
            zero 5
        }
    }

    ; Push (16-bit)
    ; Store the contents of a 16-bit register to the top of the stack
    push {src: reg16} => {
        assert(src != _SP)
        asm {
            fetch
            uop COUNT_DEC_SP                                                                                            ; dec sp to prep for push
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | (id16(src) << XFER_ASSERT) | ALU_LSB | DBUS_ASSERT_ALU | COUNT_DEC_SP  ; write src-lo to sp
            final ADDR_ASSERT_SP | DBUS_LOAD_MEM | (id16(src) << XFER_ASSERT) | ALU_MSB | DBUS_ASSERT_ALU               ; write src-hi to sp-1
            zero 4
        }
    }

    ; Pop (8-bit)
    ; Load an 8-bit register with the contents at the top of the stack
    pop {dst: reg8} => {
        asm {
            fetch
            final ADDR_ASSERT_SP | DBUS_ASSERT_MEM | (id8(dst) << DBUS_LOAD) | COUNT_INC_SP     ; read from SP into dst
            zero 6
        }
    }

    ; Pop (16-bit)
    ; Load a 16-bit register with the contents at the top of the stack
    pop {dst: reg16} => {
        assert(dst != _SP)
        asm {
            fetch
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | COUNT_INC_SP  ; read hi into t-hi
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T1                 ; read lo into t-lo
            final (id16(dst) << XFER_LOAD) | XFER_ASSERT_T                      ; move t to dst
            zero 4
        }
    }
}

#ruledef Additions {
    inc {src: acc8} => {
        asm {
            fetch
            final (xa_r8_r8(src) << XFER_ASSERT) | ALU_INC | DBUS_ASSERT_ALU | (id8(src) << DBUS_LOAD)
            zero 6
        }
    }

    inc {src: idx16} => {
        asm {
            fetch
            final inc(src) << COUNT
            zero 6
        }
    }

    inc {src: acc16} => {
        asm {
            fetch
            uop XFER_ASSERT_B_B | ALU_INC | DBUS_ASSERT_ALU | DBUS_LOAD_B
            final XFER_ASSERT_A_A | ALU_MSB_C | DBUS_ASSERT_ALU | DBUS_LOAD_A
            zero 5
        }
    }

    inc_abs => {
        assert(1 != 1)  ; TODO: figure out this inst
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2  ; read abs-hi
            uop READ_PC | DBUS_LOAD_T1  ; read abs-lo
            uop ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_T2
            uop XFER_ASSERT_T | ALU_INC | DBUS_ASSERT_ALU | DBUS_LOAD_T1
            zero 3
        }
    }

    inc_zpg => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1  ; read zpg-addr
            uop ADDR_ASSERT_DP | DBUS_ASSERT_MEM | DBUS_LOAD_T2
            uop XFER_ASSERT_T | ALU_INC | DBUS_ASSERT_ALU | DBUS_LOAD_T2
            final ADDR_ASSERT_DP | DBUS_LOAD_MEM | DBUS_ASSERT_T2
            zero 3
        }
    }

    inc_deref {src: reg16} => {
        asm {
            fetch
            uop (id16(src) << ADDR_ASSERT) | DBUS_ASSERT_MEM | DBUS_LOAD_T2
            uop XFER_ASSERT_T | ALU_INC | DBUS_ASSERT_ALU | DBUS_LOAD_T2
            final (id16(src) << ADDR_ASSERT) | DBUS_LOAD_MEM | DBUS_ASSERT_T2
            zero 4
        }
    }
}

#ruledef Subtractions {
    dec {src: acc8} => {
        asm {
            fetch
        }
    }

    dec {src: reg16} => {
        assert(src != _SP)
        asm {
            fetch
        }
    }

    dec_abs => {
        asm {
            fetch
        }
    }

    dec_zpg => {
        asm {
            fetch
        }
    }

    dec_deref {src: reg16} => {
        asm {
            fetch
        }
    }
}

#ruledef LogicalANDs {

}

#ruledef LogicalORs {

}

#ruledef LogicalXORs {

}

#ruledef LogicalNOTs {

}

#ruledef Negations {

}

#ruledef Shifts {

}

#ruledef Compares {

}

#ruledef BitTests {

}

#ruledef Jumps {
    jmp_abs => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2          ; read abs-hi
            uop READ_PC | DBUS_LOAD_T1          ; read abs-lo
            final XFER_ASSERT_T | XFER_LOAD_PC  ; move abs to PC
            zero 4
        }
    }

    jmp_rel => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1                                          ; read offset
            uop XFER_ASSERT_PC | ALU_LSB | DBUS_ASSERT_ALU | DBUS_LOAD_T2       ; move PC-lo to 8-bit side
            uop XFER_ASSERT_T | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1        ; add PC-lo and offset into t-lo
            uop XFER_ASSERT_PC | ALU_MSB_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2     ; add PC-hi and Cf into t-hi
            final XFER_ASSERT_T | XFER_LOAD_PC                                  ; move T to PC
            zero 2
        }
    }

    jmp_ind => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2          ; read vec-hi
            uop READ_PC | DBUS_LOAD_T1          ; read vec-lo
            uop XFER_ASSERT_T | XFER_LOAD_PC    ; move vec to PC
            uop READ_PC | DBUS_LOAD_T2          ; read addr-hi
            uop READ_PC | DBUS_LOAD_T1          ; read addr-lo
            final XFER_ASSERT_T | XFER_LOAD_PC  ; move addr to PC
            zero 1
        }
    }

    rts => {
        asm {
            fetch
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | COUNT_INC_SP  ; pull pc-hi
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T1 | COUNT_INC_SP  ; pull pc-lo
            final XFER_ASSERT_T | XFER_LOAD_PC                                  ; move pulled-pc to pc
            zero 4
        }
    }

    rti => {
        asm {
            fetch
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | COUNT_INC_SP                                              ; pop PC-hi
            uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T1 | COUNT_INC_SP                                              ; pop PC-lo
            final ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_SR | COUNT_INC_SP | ALU_CLI | XFER_ASSERT_T | XFER_LOAD_PC   ; pop SR, move pulled-pc to pc and enable interrupts
            zero 4
        }
    }

    jsr_abs => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T2                                                                      ; read abs-hi 
            uop READ_PC | DBUS_LOAD_T1 | COUNT_DEC_SP                                                       ; read abs-lo, dec sp for push
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_LSB | DBUS_ASSERT_ALU | COUNT_DEC_SP  ; push pc-lo, dec sp for push
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_MSB | DBUS_ASSERT_ALU                 ; push pc-hi
            final XFER_ASSERT_T | XFER_LOAD_PC                                                              ; move addr to pc
            zero 2
        }
    }

    jsr_rel => {
        asm {
            fetch
            uop READ_PC | DBUS_LOAD_T1 | COUNT_DEC_SP                                                       ; read offset and decrement sp to prepare for push
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_RHS | DBUS_ASSERT_ALU | COUNT_DEC_SP  ; push pc-lo
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_LHS | DBUS_ASSERT_ALU                 ; push pc-hi
            uop XFER_ASSERT_PC | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T2                                   ; move pc-lo to 8-bit side
            uop XFER_ASSERT_T | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1                                    ; add offset and pc-lo into t-lo
            uop XFER_ASSERT_PC | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2                                 ; move pc-hi + Cf into t-hi
            final XFER_ASSERT_T | XFER_LOAD_PC                                                              ; move t to pc
        }
    }

    jsr_ptr {ptr: idx16} => {
        asm {
            fetch
            uop COUNT_DEC_SP                                                                                ; dec sp to prepare for push
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_LSB | DBUS_ASSERT_ALU | COUNT_DEC_SP  ; push pc-lo and dec sp to prep for next push
            uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_MSB | DBUS_ASSERT_ALU                 ; push pc-hi
            final (id16(ptr) << XFER_ASSERT) | XFER_LOAD_PC                                                 ; move ptr-val into pc
        }
    }
}
