#include "ctrl.asm"

#bits 32
#labelalign 8 * 32

; Consider "LOAD A [SP]" and/or "STORE A [SP]"?

; USE A FULL DESCENDING STACK
; So for push:
;   - dec
;   - write
; And for pop:
;   - read
;   - inc

; BIG ENDIAN - So for FD Stack, Push Lo first then Hi
;                               Pull Hi first then Lo
;            - So for ABS Addr, Read Hi first then Lo
;                               Write Hi first then Lo

; Temp Register
; T2 - High Byte
; T1 - Low Byte

#bank mode00  ; NRM Mode
brk:  ; Opcode 0x00
    fetch
    final_brk
nop:  ; Opcode 0x01
    fetch
    final
wai:  ; Opcode 0x02
    ; TBD
ex1:  ; Opcode 0x03
    fetch
    final_ext1
ex2:  ; Opcode 0x04
    fetch
    final_ext2
swi_x:  ; Opcode 0x05
    swi x
swi_y:  ; Opcode 0x06
    swi y

mov_a_b:  ; Opcode 0x07
    mov a b
mov_a_c:  ; Opcode 0x08
    mov a c
mov_a_d:  ; Opcode 0x09
    mov a d
mov_b_a:  ; Opcode 0x0A
    mov b a
mov_b_c:  ; Opcode 0x0B
    mov b c
mov_b_d:  ; Opcode 0x0C
    mov b d
mov_c_a:  ; Opcode 0x0D
    mov c a
mov_c_b:  ; Opcode 0x0E
    mov c b
mov_c_d:  ; Opcode 0x0F
    mov c d
mov_d_a:  ; Opcode 0x10
    mov d a
mov_d_b:  ; Opcode 0x11
    mov d b
mov_d_c:  ; Opcode 0x12
    mov d c

mov_sp_x:  ; Opcode 0x13
    mov sp x
mov_sp_y:  ; Opcode 0x14
    mov sp y
mov_sp_e:  ; Opcode 0x15
    mov sp e
mov_x_y:  ; Opcode 0x16
    mov x y
mov_x_e:  ; Opcode 0x17
    mov x e
mov_x_sp:  ; Opcode 0x18
    mov x sp
mov_y_x:  ; Opcode 0x19
    mov y x
mov_y_e:  ; Opcode 0x1A
    mov y e
mov_y_sp:  ; Opcode 0x1B
    mov y sp
mov_e_x:  ; Opcode 0x1C
    mov e x
mov_e_y:  ; Opcode 0x1D
    mov e y
mov_e_sp:  ; Opcode 0x1E
    mov e sp

load_a_imm:  ; Opcode 0x1F
    load_imm a
load_a_abs:  ; Opcode 0x20
    load_abs a
load_a_zpg:  ; Opcode 0x21
    load_zpg a
load_a_a_index_zpg:  ; Opcode 0x22
    fetch
    uop READ_PC | DBUS_LOAD_T1
    uop ALU_ADD | XFER_ASSERT_A_T1 | DBUS_ASSERT_ALU | DBUS_LOAD_T1
    final ADDR_ASSERT_DP | DBUS_ASSERT_MEM | DBUS_LOAD_A
load_a_b_index_zpg:  ; Opcode 0x23
    fetch
    uop READ_PC | DBUS_LOAD_T1
    uop ALU_ADD | XFER_ASSERT_B_T1 | DBUS_ASSERT_ALU | DBUS_LOAD_T1
    final ADDR_ASSERT_DP | DBUS_ASSERT_MEM | DBUS_LOAD_A
load_a_x:  ; Opcode 0x24
    load_ptr a x
load_a_y:  ; Opcode 0x25
    load_ptr a y
load_a_e:  ; Opcode 0x26
    load_ptr a e
load_a_const_index_x:  ; Opcode 0x27
    ; [A] = [[X + [PC]++]]
    fetch
    uop READ_PC | DBUS_LOAD_A  ; read offset into A
    uop XFER_ASSERT_X | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move X-Lo into T1
    uop XFER_ASSERT_A_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and X-Lo into T1
    uop XFER_ASSERT_X | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add X-Hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_const_index_y:  ; Opcode 0x28
    ; [A] = [[Y + [PC]++]]
    fetch
    uop READ_PC | DBUS_LOAD_A  ; read offset into A
    uop XFER_ASSERT_Y | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move Y-Lo into T1
    uop XFER_ASSERT_A_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and Y-Lo into T1
    uop XFER_ASSERT_Y | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add Y-Hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_const_index_e:  ; Opcode 0x29
    ; ; [A] = [[E + [PC]++]]
    fetch
    uop READ_PC | DBUS_LOAD_T2  ; read offset into A
    uop XFER_ASSERT_E | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move E-Lo into T1
    uop XFER_ASSERT_T | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and X-Lo into T1
    uop XFER_ASSERT_E | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add E-Hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_const_index_sp:  ; Opcode 0x2A
    ; [A] = [[SP + [PC]++]]
    fetch
    uop READ_PC | DBUS_LOAD_A  ; read offset into A
    uop XFER_ASSERT_SP | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move SP-Lo into T1
    uop XFER_ASSERT_A_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and X-Lo into T1
    uop XFER_ASSERT_SP | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add SP-Hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_a_index_x:  ; Opcode 0x2B
    ; [A] = [[X + [A]]]
    fetch
    uop XFER_ASSERT_X | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move X-lo into T1
    uop XFER_ASSERT_A_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and X-lo into T1
    uop XFER_ASSERT_X | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add X-hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_a_index_y:  ; Opcode 0x2C
    ; [A] = [[Y + [A]]]
    fetch
    uop XFER_ASSERT_Y | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move Y-lo into T1
    uop XFER_ASSERT_A_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and Y-lo into T1
    uop XFER_ASSERT_Y | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add Y-hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_a_index_sp:  ; Opcode 0x2D
    ; [A] = [[SP + [A]]]
    fetch
    uop XFER_ASSERT_SP | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move SP-lo into T1
    uop XFER_ASSERT_A_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and SP-lo into T1
    uop XFER_ASSERT_SP | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add SP-hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_b_index_x:  ; Opcode 0x2E
    ; [A] = [[X + [B]]]
    fetch
    uop XFER_ASSERT_X | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move X-lo into T1
    uop XFER_ASSERT_B_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and SP-lo into T1
    uop XFER_ASSERT_X | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add X-hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_b_index_y:  ; Opcode 0x2F
    ; [A] = [[Y + [B]]]
    fetch
    uop XFER_ASSERT_Y | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move Y-lo into T1
    uop XFER_ASSERT_B_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and SP-lo into T1
    uop XFER_ASSERT_Y | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add Y-hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A
load_a_b_index_sp:  ; Opcode 0x30
    ; [A] = [[SP + [B]]]
    fetch
    uop XFER_ASSERT_SP | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; move SP-lo into T1
    uop XFER_ASSERT_B_T1 | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1  ; add offset and SP-lo into T1
    uop XFER_ASSERT_SP | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2  ; add SP-hi and Cf into T2
    final ADDR_ASSERT_T | DBUS_ASSERT_MEM | DBUS_LOAD_A  ; read from temp into A

load_b_imm:  ; Opcode 0x31
    load_imm b
load_b_abs:  ; Opcode 0x32
    load_abs b
load_b_zpg:  ; Opcode 0x33
    load_zpg b
load_b_x:  ; Opcode 0x34
    load_ptr b x
load_b_y:  ; Opcode 0x35
    load_ptr b y
load_b_e:  ; Opcode 0x36
    load_ptr b e

load_c_imm:  ; Opcode 0x37
    load_imm c
load_c_abs:  ; Opcode 0x38
    load_abs c
load_c_zpg:  ; Opcode 0x39
    load_zpg c
load_c_x:  ; Opcode 0x3A
    load_ptr c x
load_c_y:  ; Opcode 0x3B
    load_ptr c y
load_c_e:  ; Opcode 0x3C
    load_ptr c e

load_d_imm:  ; Opcode 0x3D
    load_imm d
load_d_abs:  ; Opcode 0x3E
    load_abs d
load_d_zpg:  ; Opcode 0x3F
    load_zpg d
load_d_x:  ; Opcode 0x40
    load_ptr d x
load_d_y:  ; Opcode 0x41
    load_ptr d y
load_d_e:  ; Opcode 0x42
    load_ptr d e

store_a_zpg:  ; Opcode 0x43
    store_zpg a
store_a_abs:  ; Opcode 0x44
    store_abs a
store_a_x:  ; Opcode 0x45
    store_ptr a x
store_a_y:  ; Opcode 0x46
    store_ptr a y
store_a_e:  ; Opcode 0x47
    store_ptr a e
store_a_const_index_x:  ; Opcode 0x48
store_a_const_index_y:  ; Opcode 0x49
store_a_const_index_e:  ; Opcode 0x4A
store_a_const_index_sp:  ; Opcode 0x4B
store_a_a_index_x:  ; Opcode 0x4C
store_a_a_index_y:  ; Opcode 0x4D
store_a_a_index_sp:  ; Opcode 0x4E
store_a_b_index_x:  ; Opcode 0x4F
store_a_b_index_y:  ; Opcode 0x50
store_a_b_index_sp:  ; Opcode 0x51

store_b_zpg:  ; Opcode 0x52
    store_zpg b
store_b_abs:  ; Opcode 0x53
    store_abs b
store_b_x:  ; Opcode 0x54
    store_ptr b x
store_b_y:  ; Opcode 0x55
    store_ptr b y
store_b_e:  ; Opcode 0x56
    store_ptr b e

store_c_zpg:  ; Opcode 0x57
    store_zpg c
store_c_abs:  ; Opcode 0x58
    store_abs c
store_c_x:  ; Opcode 0x59
    store_ptr c x
store_c_y:  ; Opcode 0x5A
    store_ptr c y
store_c_e:  ; Opcode 0x5B
    store_ptr c e

store_d_zpg:  ; Opcode 0x5C
    store_zpg d
store_d_abs:  ; Opcode 0x5D
    store_abs d
store_d_x:  ; Opcode 0x5E
    store_ptr d x
store_d_y:  ; Opcode 0x5F
    store_ptr d y
store_d_e:  ; Opcode 0x60
    store_ptr d e

load_x_imm:  ; Opcode 0x61
    load_imm x
load_x_abs:  ; Opcode 0x62
    load_abs x
load_x_zpg:  ; Opcode 0x63
    load_zpg x
load_x_x:  ; Opcode 0x64
    load_ptr x x
load_x_y:  ; Opcode 0x65
    load_ptr x y
load_x_e:  ; Opcode 0x66
    load_ptr x e

load_y_imm:  ; Opcode 0x67
    load_imm y
load_y_abs:  ; Opcode 0x68
    load_abs y
load_y_zpg:  ; Opcode 0x69
    load_zpg y
load_y_x:  ; Opcode 0x6A
    load_ptr y x
load_y_y:  ; Opcode 0x6B
    load_ptr y y
load_y_e:  ; Opcode 0x6C
    load_ptr y e

load_e_imm:  ; Opcode 0x6D
    load_imm e
load_e_abs:  ; Opcode 0x6E
    load_abs e
load_e_zpg:  ; Opcode 0x6F
    load_zpg e
load_e_x:  ; Opcode 0x70
    load_ptr e x
load_e_y:  ; Opcode 0x71
    load_ptr e y
load_e_e:  ; Opcode 0x72
    load_ptr e e
load_e_const_index_x:  ; Opcode 0x73
    fetch
    uop READ_PC | DBUS_LOAD_T1  ; read offset into A
load_e_const_index_y:  ; Opcode 0x74
load_e_const_index_sp:  ; Opcode 0x75

store_x_zpg:  ; Opcode 0x76
    store_zpg x
store_x_abs:  ; Opcode 0x77
    store_abs x
store_x_y:  ; Opcode 0x78
store_x_e:  ; Opcode 0x79

store_y_zpg:  ; Opcode 0x7A
store_y_abs:  ; Opcode 0x7B
store_y_x:  ; Opcode 0x7C
store_y_e:  ; Opcode 0x7D

store_e_zpg:  ; Opcode 0x7E
store_e_abs:  ; Opcode 0x7F
store_e_x:  ; Opcode 0x80
store_e_y:  ; Opcode 0x81
store_e_const_index_x:  ; Opcode 0x82
store_e_const_index_y:  ; Opcode 0x83
store_e_const_index_sp:  ; Opcode 0x84
store_e_a_index_x:  ; Opcode 0x85
store_e_a_index_y:  ; Opcode 0x86
store_e_a_index_sp:  ; Opcode 0x87
store_e_b_index_x:  ; Opcode 0x88
store_e_b_index_y:  ; Opcode 0x89
store_e_b_index_sp:  ; Opcode 0x8A

inc_a:  ; Opcode 0x8B
inc_b:  ; Opcode 0x8C
inc_x:  ; Opcode 0x8D
inc_y:  ; Opcode 0x8E
inc_e:  ; Opcode 0x8F

dec_a:  ; Opcode 0x90
dec_b:  ; Opcode 0x91
dec_x:  ; Opcode 0x92
dec_y:  ; Opcode 0x93
dec_e:  ; Opcode 0x94
dec_abs:  ; Opcode 0x95
dec_zpg:  ; Opcode 0x96
dec_deref_x:  ; Opcode 0x97
dec_deref_y:  ; Opcode 0x98
dec_deref_e:  ; Opcode 0x99
dec_deref_sp:  ; Opcode 0x9A

add_a_imm:  ; Opcode 0x9B
add_a_zpg:  ; Opcode 0x9C
add_a_abs:  ; Opcode 0x9D
add_a_deref_x:  ; Opcode 0x9E
add_a_deref_y:  ; Opcode 0x9F
add_a_deref_sp:  ; Opcode 0xA0
add_a_b:  ; Opcode 0xA1
add_a_c:  ; Opcode 0xA2
add_a_d:  ; Opcode 0xA3

add_e_imm:  ; Opcode 0xA4
add_e_zpg:  ; Opcode 0xA5
add_e_abs:  ; Opcode 0xA6
add_e_x:  ; Opcode 0xA7
add_e_y:  ; Opcode 0xA8
add_e_sp:  ; Opcode 0xA9
add_e_deref_x:  ; Opcode 0xAA
add_e_deref_y:  ; Opcode 0xAB
add_e_deref_sp:  ; Opcode 0xAC

sub_a_imm:  ; Opcode 0xAD
sub_a_zpg:  ; Opcode 0xAE
sub_a_abs:  ; Opcode 0xAF
sub_a_deref_x:  ; Opcode 0xB0
sub_a_deref_y:  ; Opcode 0xB1
sub_a_deref_sp:  ; Opcode 0xB2
sub_a_b:  ; Opcode 0xB3
sub_a_c:  ; Opcode 0xB4
sub_a_d:  ; Opcode 0xB5

sub_e_imm:  ; Opcode 0xB6
sub_e_zpg:  ; Opcode 0xB7
sub_e_abs:  ; Opcode 0xB8
sub_e_x:  ; Opcode 0xB9
sub_e_y:  ; Opcode 0xBA
sub_e_sp:  ; Opcode 0xBB
sub_e_deref_x:  ; Opcode 0xBC
sub_e_deref_y:  ; Opcode 0xBD
sub_e_deref_sp:  ; Opcode 0xBE

cmp_a_imm:  ; Opcode 0xBF
cmp_a_zpg:  ; Opcode 0xC0
cmp_a_abs:  ; Opcode 0xC1
cmp_a_deref_x:  ; Opcode 0xC2
cmp_a_deref_y:  ; Opcode 0xC3
cmp_a_deref_sp:  ; Opcode 0xC4
cmp_a_b:  ; Opcode 0xC5
cmp_a_c:  ; Opcode 0xC6
cmp_a_d:  ; Opcode 0xC7

cmp_e_imm:  ; Opcode 0xC8
cmp_e_zpg:  ; Opcode 0xC9
cmp_e_abs:  ; Opcode 0xCA
cmp_e_x:  ; Opcode 0xCB
cmp_e_y:  ; Opcode 0xCC
cmp_e_sp:  ; Opcode 0xCD
cmp_e_deref_x:  ; Opcode 0xCE
cmp_e_deref_y:  ; Opcode 0xCF
cmp_e_deref_sp:  ; Opcode 0xD0

tst_a:  ; Opcode 0xD1
tst_e:  ; Opcode 0xD2
tst_zpg:  ; Opcode 0xD3
tst_abs:  ; Opcode 0xD4
tst_deref_e:  ; Opcode 0xD5

push_a:  ; Opcode 0xD6
    push a
push_b:  ; Opcode 0xD7
    push b
push_c:  ; Opcode 0xD8
    push c
push_d:  ; Opcode 0xD9
    push d

push_e:  ; Opcode 0xDA
    push e
push_x:  ; Opcode 0xDB
    push x
push_y:  ; Opcode 0xDC
    push y

pop_a:  ; Opcode 0xDD
    pop a
pop_b:  ; Opcode 0xDE
    pop b
pop_c:  ; Opcode 0xDF
    pop c
pop_d:  ; Opcode 0xE0
    pop d

pop_e:  ; Opcode 0xE1
    pop e
pop_x:  ; Opcode 0xE2
    pop x
pop_y:  ; Opcode 0xE3
    pop y

jmp_rel:  ; Opcode 0xE4
    fetch
    uop READ_PC | DBUS_LOAD_T1
    uop XFER_ASSERT_PC | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T2
    uop XFER_ASSERT_T | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1
    uop XFER_ASSERT_PC | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2
    final XFER_ASSERT_T | XFER_LOAD_PC

jmp_ind:  ; Opcode 0xE5
    fetch
    uop READ_PC | DBUS_LOAD_T2
    uop READ_PC | DBUS_LOAD_T1
    uop XFER_ASSERT_T | XFER_LOAD_PC
    uop READ_PC | DBUS_LOAD_T2
    uop READ_PC | DBUS_LOAD_T1
    final XFER_ASSERT_T | XFER_LOAD_PC

jsr_abs:  ; 0xE6
    fetch
    uop READ_PC | DBUS_LOAD_T1                                                                      ; Read ABS-hi 
    uop READ_PC | DBUS_LOAD_T2 | COUNT_DEC_SP                                                       ; Read ABS-lo, dec SP for push
    uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_RHS | DBUS_ASSERT_ALU | COUNT_DEC_SP  ; Push PC-lo, dec SP for push
    uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_LHS | DBUS_ASSERT_ALU                 ; Push PC-hi
    final XFER_ASSERT_T | XFER_LOAD_PC                                                              ; Move addr to PC

jsr_rel:  ; Opcode 0xE7
    fetch
    uop READ_PC | DBUS_LOAD_T1 | COUNT_DEC_SP                                                       ; read offset and decrement SP to prepare for push
    uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_RHS | DBUS_ASSERT_ALU | COUNT_DEC_SP  ; Push PC-lo
    uop ADDR_ASSERT_SP | DBUS_LOAD_MEM | XFER_ASSERT_PC | ALU_LHS | DBUS_ASSERT_ALU                 ; Push PC-hi
    uop XFER_ASSERT_PC | ALU_RHS | DBUS_ASSERT_ALU | DBUS_LOAD_T2                                   ; move PC-lo to 8-bit side
    uop XFER_ASSERT_T | ALU_ADD | DBUS_ASSERT_ALU | DBUS_LOAD_T1                                    ; add offset and PC-lo into T1 (T-lo)
    uop XFER_ASSERT_PC | ALU_LHS_C | DBUS_ASSERT_ALU | DBUS_LOAD_T2                                 ; move PC-Hi + Cf into T2 (T-hi)
    final XFER_ASSERT_T | XFER_LOAD_PC                                                              ; move T to PC

jsr_ind:  ; Opcode 0xE8

rts:  ; Opcode 0xE9
    fetch
    uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | COUNT_INC_SP  ; pull PC-hi
    uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T1 | COUNT_INC_SP  ; pull PC-lo
    final XFER_ASSERT_T | XFER_LOAD_PC                                  ; move to PC
rti:  ; Opcode 0xEA
    fetch
    uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T2 | COUNT_INC_SP  ; pop PC-hi
    uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_T1 | COUNT_INC_SP; pop PC-lo
    uop ADDR_ASSERT_SP | DBUS_ASSERT_MEM | DBUS_LOAD_SR | COUNT_INC_SP; pop SR
    final ALU_CLI | XFER_ASSERT_T | XFER_LOAD_PC

jo_rel:  ; Opcode 0xEB
jo_ind:  ; Opcode 0xEC
jno_rel:  ; Opcode 0xED
jno_ind:  ; Opcode 0xEE
jn_rel:  ; Opcode 0xEF
jn_ind:  ; Opcode 0xF0
jp_rel:  ; Opcode 0xF1
jp_ind:  ; Opcode 0xF2
jz_rel:  ; Opcode 0xF3
jz_ind:  ; Opcode 0xF4
jnz_rel:  ; Opcode 0xF5
jnz_ind:  ; Opcode 0xF6
jc_rel:  ; Opcode 0xF7
jc_ind:  ; Opcode 0xF8
jnc_rel:  ; Opcode 0xF9
jnc_ind:  ; Opcode 0xFA
ja_rel:  ; Opcode 0xFB
ja_ind:  ; Opcode 0xFC
jna_rel:  ; Opcode 0xFD
jna_ind:  ; Opcode 0xFE

#bank mode01  ; EX1 Mode
clc:  ; Opcode 0x00
cli:  ; Opcode 0x01
clv:  ; Opcode 0x02
sec:  ; Opcode 0x03
sei:  ; Opcode 0x04
mov_a_dp:  ; Opcode 0x05
mov_b_dp:  ; Opcode 0x06
mov_c_dp:  ; Opcode 0x07
mov_d_dp:  ; Opcode 0x08
mov_dp_a:  ; Opcode 0x09
mov_dp_b:  ; Opcode 0x0a
mov_dp_c:  ; Opcode 0x0b
mov_dp_d:  ; Opcode 0x0c
load_b_a_index_zpg:  ; Opcode 0x0d
load_b_b_index_zpg:  ; Opcode 0x0e
load_b_const_index_x:  ; Opcode 0x0f
load_b_const_index_y:  ; Opcode 0x10
load_b_const_index_e:  ; Opcode 0x11
load_b_const_index_sp:  ; Opcode 0x12
load_b_a_index_x:  ; Opcode 0x13
load_b_a_index_y:  ; Opcode 0x14
load_b_a_index_sp:  ; Opcode 0x15
load_b_b_index_x:  ; Opcode 0x16
load_b_b_index_y:  ; Opcode 0x17
load_b_b_index_sp:  ; Opcode 0x18
load_c_a_index_zpg:  ; Opcode 0x19
load_c_b_index_zpg:  ; Opcode 0x1a
load_c_const_index_x:  ; Opcode 0x1b
load_c_const_index_y:  ; Opcode 0x1c
load_c_const_index_e:  ; Opcode 0x1d
load_c_const_index_sp:  ; Opcode 0x1e
load_c_a_index_x:  ; Opcode 0x1f
load_c_a_index_y:  ; Opcode 0x20
load_c_a_index_sp:  ; Opcode 0x21
load_c_b_index_x:  ; Opcode 0x22
load_c_b_index_y:  ; Opcode 0x23
load_c_b_index_sp:  ; Opcode 0x24
load_d_a_index_zpg:  ; Opcode 0x25
load_d_b_index_zpg:  ; Opcode 0x26
load_d_const_index_x:  ; Opcode 0x27
load_d_const_index_y:  ; Opcode 0x28
load_d_const_index_e:  ; Opcode 0x29
load_d_const_index_sp:  ; Opcode 0x2a
load_d_a_index_x:  ; Opcode 0x2b
load_d_a_index_y:  ; Opcode 0x2c
load_d_a_index_sp:  ; Opcode 0x2d
load_d_b_index_x:  ; Opcode 0x2e
load_d_b_index_y:  ; Opcode 0x2f
load_d_b_index_sp:  ; Opcode 0x30
store_b_const_index_x:  ; Opcode 0x31
store_b_const_index_y:  ; Opcode 0x32
store_b_const_index_e:  ; Opcode 0x33
store_b_const_index_sp:  ; Opcode 0x34
store_b_a_index_x:  ; Opcode 0x35
store_b_a_index_y:  ; Opcode 0x36
store_b_a_index_sp:  ; Opcode 0x37
store_b_b_index_x:  ; Opcode 0x38
store_b_b_index_y:  ; Opcode 0x39
store_b_b_index_sp:  ; Opcode 0x3a
store_c_const_index_x:  ; Opcode 0x3b
store_c_const_index_y:  ; Opcode 0x3c
store_c_const_index_e:  ; Opcode 0x3d
store_c_const_index_sp:  ; Opcode 0x3e
store_c_a_index_x:  ; Opcode 0x3f
store_c_a_index_y:  ; Opcode 0x40
store_c_a_index_sp:  ; Opcode 0x41
store_c_b_index_x:  ; Opcode 0x42
store_c_b_index_y:  ; Opcode 0x43
store_c_b_index_sp:  ; Opcode 0x44
store_d_const_index_x:  ; Opcode 0x45
store_d_const_index_y:  ; Opcode 0x46
store_d_const_index_e:  ; Opcode 0x47
store_d_const_index_sp:  ; Opcode 0x48
store_d_a_index_x:  ; Opcode 0x49
store_d_a_index_y:  ; Opcode 0x4a
store_d_a_index_sp:  ; Opcode 0x4b
store_d_b_index_x:  ; Opcode 0x4c
store_d_b_index_y:  ; Opcode 0x4d
store_d_b_index_sp:  ; Opcode 0x4e
load_x_const_index_x:  ; Opcode 0x4f
load_x_const_index_y:  ; Opcode 0x50
load_x_const_index_e:  ; Opcode 0x51
load_x_const_index_sp:  ; Opcode 0x52
load_x_a_index_x:  ; Opcode 0x53
load_x_a_index_y:  ; Opcode 0x54
load_x_a_index_sp:  ; Opcode 0x55
load_x_b_index_x:  ; Opcode 0x56
load_x_b_index_y:  ; Opcode 0x57
load_x_b_index_sp:  ; Opcode 0x58
load_y_const_index_x:  ; Opcode 0x59
load_y_const_index_y:  ; Opcode 0x5a
load_y_const_index_e:  ; Opcode 0x5b
load_y_const_index_sp:  ; Opcode 0x5c
load_y_a_index_x:  ; Opcode 0x5d
load_y_a_index_y:  ; Opcode 0x5e
load_y_a_index_sp:  ; Opcode 0x5f
load_y_b_index_x:  ; Opcode 0x60
load_y_b_index_y:  ; Opcode 0x61
load_y_b_index_sp:  ; Opcode 0x62
store_x_const_index_y:  ; Opcode 0x63
store_x_const_index_e:  ; Opcode 0x64
store_x_const_index_sp:  ; Opcode 0x65
store_x_a_index_y:  ; Opcode 0x66
store_x_a_index_e:  ; Opcode 0x67
store_x_a_index_sp:  ; Opcode 0x68
store_x_b_index_y:  ; Opcode 0x69
store_x_b_index_e:  ; Opcode 0x6a
store_x_b_index_sp:  ; Opcode 0x6b
store_y_const_index_x:  ; Opcode 0x6c
store_y_const_index_e:  ; Opcode 0x6d
store_y_const_index_sp:  ; Opcode 0x6e
store_y_a_index_x:  ; Opcode 0x6f
store_y_a_index_e:  ; Opcode 0x70
store_y_a_index_sp:  ; Opcode 0x71
store_y_b_index_x:  ; Opcode 0x72
store_y_b_index_e:  ; Opcode 0x73
store_y_b_index_sp:  ; Opcode 0x74
inc_abs:  ; Opcode 0x75
inc_zpg:  ; Opcode 0x76
inc_deref_x:  ; Opcode 0x77
inc_deref_y:  ; Opcode 0x78
inc_deref_e:  ; Opcode 0x79
inc_deref_sp:  ; Opcode 0x7a
add_b_imm:  ; Opcode 0x7b
add_b_zpg:  ; Opcode 0x7c
add_b_abs:  ; Opcode 0x7d
add_b_deref_x:  ; Opcode 0x7e
add_b_deref_y:  ; Opcode 0x7f
add_b_deref_sp:  ; Opcode 0x80
add_b_a:  ; Opcode 0x81
add_b_c:  ; Opcode 0x82
add_b_d:  ; Opcode 0x83
adc_a_imm:  ; Opcode 0x84
adc_a_zpg:  ; Opcode 0x85
adc_a_abs:  ; Opcode 0x86
adc_a_deref_x:  ; Opcode 0x87
adc_a_deref_y:  ; Opcode 0x88
adc_a_deref_sp:  ; Opcode 0x89
adc_a_b:  ; Opcode 0x8a
adc_a_c:  ; Opcode 0x8b
adc_a_d:  ; Opcode 0x8c
adc_b_imm:  ; Opcode 0x8d
adc_b_zpg:  ; Opcode 0x8e
adc_b_abs:  ; Opcode 0x8f
adc_b_deref_x:  ; Opcode 0x90
adc_b_deref_y:  ; Opcode 0x91
adc_b_deref_sp:  ; Opcode 0x92
adc_b_a:  ; Opcode 0x93
adc_b_c:  ; Opcode 0x94
adc_b_d:  ; Opcode 0x95
adc_e_imm:  ; Opcode 0x96
adc_e_zpg:  ; Opcode 0x97
adc_e_abs:  ; Opcode 0x98
adc_e_x:  ; Opcode 0x99
adc_e_y:  ; Opcode 0x9a
adc_e_sp:  ; Opcode 0x9b
adc_e_deref_x:  ; Opcode 0x9c
adc_e_deref_y:  ; Opcode 0x9d
adc_e_deref_sp:  ; Opcode 0x9e
sub_b_imm:  ; Opcode 0x9f
sub_b_zpg:  ; Opcode 0xa0
sub_b_abs:  ; Opcode 0xa1
sub_b_deref_x:  ; Opcode 0xa2
sub_b_deref_y:  ; Opcode 0xa3
sub_b_deref_sp:  ; Opcode 0xa4
sub_b_a:  ; Opcode 0xa5
sub_b_c:  ; Opcode 0xa6
sub_b_d:  ; Opcode 0xa7
sbb_a_imm:  ; Opcode 0xa8
sbb_a_zpg:  ; Opcode 0xa9
sbb_a_abs:  ; Opcode 0xaa
sbb_a_deref_x:  ; Opcode 0xab
sbb_a_deref_y:  ; Opcode 0xac
sbb_a_deref_sp:  ; Opcode 0xad
sbb_a_b:  ; Opcode 0xae
sbb_a_c:  ; Opcode 0xaf
sbb_a_d:  ; Opcode 0xb0
sbb_b_imm:  ; Opcode 0xb1
sbb_b_zpg:  ; Opcode 0xb2
sbb_b_abs:  ; Opcode 0xb3
sbb_b_deref_x:  ; Opcode 0xb4
sbb_b_deref_y:  ; Opcode 0xb5
sbb_b_deref_sp:  ; Opcode 0xb6
sbb_b_a:  ; Opcode 0xb7
sbb_b_c:  ; Opcode 0xb8
sbb_b_d:  ; Opcode 0xb9
sbb_e_imm:  ; Opcode 0xba
sbb_e_zpg:  ; Opcode 0xbb
sbb_e_abs:  ; Opcode 0xbc
sbb_e_x:  ; Opcode 0xbd
sbb_e_y:  ; Opcode 0xbe
sbb_e_sp:  ; Opcode 0xbf
sbb_e_deref_x:  ; Opcode 0xc0
sbb_e_deref_y:  ; Opcode 0xc1
sbb_e_deref_sp:  ; Opcode 0xc2
and_a_imm:  ; Opcode 0xc3
and_a_zpg:  ; Opcode 0xc4
and_a_abs:  ; Opcode 0xc5
and_a_deref_x:  ; Opcode 0xc6
and_a_deref_y:  ; Opcode 0xc7
and_a_deref_sp:  ; Opcode 0xc8
and_a_b:  ; Opcode 0xc9
and_a_c:  ; Opcode 0xca
and_a_d:  ; Opcode 0xcb
and_b_imm:  ; Opcode 0xcc
and_b_zpg:  ; Opcode 0xcd
and_b_abs:  ; Opcode 0xce
and_b_deref_x:  ; Opcode 0xcf
and_b_deref_y:  ; Opcode 0xd0
and_b_deref_sp:  ; Opcode 0xd1
and_b_a:  ; Opcode 0xd2
and_b_c:  ; Opcode 0xd3
and_b_d:  ; Opcode 0xd4
and_e_imm:  ; Opcode 0xd5
and_e_zpg:  ; Opcode 0xd6
and_e_abs:  ; Opcode 0xd7
and_e_x:  ; Opcode 0xd8
and_e_y:  ; Opcode 0xd9
and_e_sp:  ; Opcode 0xda
and_e_deref_x:  ; Opcode 0xdb
and_e_deref_y:  ; Opcode 0xdc
and_e_deref_sp:  ; Opcode 0xdd
or_a_imm:  ; Opcode 0xde
or_a_zpg:  ; Opcode 0xdf
or_a_abs:  ; Opcode 0xe0
or_a_deref_x:  ; Opcode 0xe1
or_a_deref_y:  ; Opcode 0xe2
or_a_deref_sp:  ; Opcode 0xe3
or_a_b:  ; Opcode 0xe4
or_a_c:  ; Opcode 0xe5
or_a_d:  ; Opcode 0xe6
or_b_imm:  ; Opcode 0xe7
or_b_zpg:  ; Opcode 0xe8
or_b_abs:  ; Opcode 0xe9
or_b_deref_x:  ; Opcode 0xea
or_b_deref_y:  ; Opcode 0xeb
or_b_deref_sp:  ; Opcode 0xec
or_b_a:  ; Opcode 0xed
or_b_c:  ; Opcode 0xee
or_b_d:  ; Opcode 0xef
or_e_imm:  ; Opcode 0xf0
or_e_zpg:  ; Opcode 0xf1
or_e_abs:  ; Opcode 0xf2
or_e_x:  ; Opcode 0xf3
or_e_y:  ; Opcode 0xf4
or_e_sp:  ; Opcode 0xf5
or_e_deref_x:  ; Opcode 0xf6
or_e_deref_y:  ; Opcode 0xf7
or_e_deref_sp:  ; Opcode 0xf8
xor_a_imm:  ; Opcode 0xf9
xor_a_zpg:  ; Opcode 0xfa
xor_a_abs:  ; Opcode 0xfb
xor_a_deref_x:  ; Opcode 0xfc
xor_a_deref_y:  ; Opcode 0xfd
xor_a_deref_sp:  ; Opcode 0xfe
xor_a_a:  ; Opcode 0xff

#bank mode10  ; RST Mode
; insert reset sequence here

#bank mode11  ; EX2 Mode
xor_a_b:  ; Opcode 0x00
xor_a_c:  ; Opcode 0x01
xor_a_d:  ; Opcode 0x02
xor_b_imm:  ; Opcode 0x03
xor_b_zpg:  ; Opcode 0x04
xor_b_abs:  ; Opcode 0x05
xor_b_deref_x:  ; Opcode 0x06
xor_b_deref_y:  ; Opcode 0x07
xor_b_deref_sp:  ; Opcode 0x08
xor_b_a:  ; Opcode 0x09
xor_b_b:  ; Opcode 0x0a
xor_b_c:  ; Opcode 0x0b
xor_b_d:  ; Opcode 0x0c
xor_e_imm:  ; Opcode 0x0d
xor_e_zpg:  ; Opcode 0x0e
xor_e_abs:  ; Opcode 0x0f
xor_e_x:  ; Opcode 0x10
xor_e_y:  ; Opcode 0x11
xor_e_sp:  ; Opcode 0x12
xor_e_deref_x:  ; Opcode 0x13
xor_e_deref_y:  ; Opcode 0x14
xor_e_deref_sp:  ; Opcode 0x15
not_a:  ; Opcode 0x16
not_b:  ; Opcode 0x17
not_e:  ; Opcode 0x18
not_zpg:  ; Opcode 0x19
not_abs:  ; Opcode 0x1a
not_deref_x:  ; Opcode 0x1b
not_deref_y:  ; Opcode 0x1c
not_deref_e:  ; Opcode 0x1d
not_deref_sp:  ; Opcode 0x1e
neg_a:  ; Opcode 0x1f
neg_b:  ; Opcode 0x20
neg_e:  ; Opcode 0x21
neg_zpg:  ; Opcode 0x22
neg_abs:  ; Opcode 0x23
neg_deref_x:  ; Opcode 0x24
neg_deref_y:  ; Opcode 0x25
neg_deref_e:  ; Opcode 0x26
neg_deref_sp:  ; Opcode 0x27
asr_a:  ; Opcode 0x28
asr_b:  ; Opcode 0x29
asr_e:  ; Opcode 0x2a
asr_zpg:  ; Opcode 0x2b
asr_abs:  ; Opcode 0x2c
asr_deref_x:  ; Opcode 0x2d
asr_deref_y:  ; Opcode 0x2e
asr_deref_e:  ; Opcode 0x2f
asr_deref_sp:  ; Opcode 0x30
shrc_a:  ; Opcode 0x31
shrc_b:  ; Opcode 0x32
shrc_e:  ; Opcode 0x33
shrc_zpg:  ; Opcode 0x34
shrc_abs:  ; Opcode 0x35
shrc_deref_x:  ; Opcode 0x36
shrc_deref_y:  ; Opcode 0x37
shrc_deref_e:  ; Opcode 0x38
shrc_deref_sp:  ; Opcode 0x39
shr_a:  ; Opcode 0x3a
shr_b:  ; Opcode 0x3b
shr_e:  ; Opcode 0x3c
shr_zpg:  ; Opcode 0x3d
shr_abs:  ; Opcode 0x3e
shr_deref_x:  ; Opcode 0x3f
shr_deref_y:  ; Opcode 0x40
shr_deref_e:  ; Opcode 0x41
shr_deref_sp:  ; Opcode 0x42
shlc_a:  ; Opcode 0x43
shlc_b:  ; Opcode 0x44
shlc_e:  ; Opcode 0x45
shlc_zpg:  ; Opcode 0x46
shlc_abs:  ; Opcode 0x47
shlc_deref_x:  ; Opcode 0x48
shlc_deref_y:  ; Opcode 0x49
shlc_deref_e:  ; Opcode 0x4a
shlc_deref_sp:  ; Opcode 0x4b
shl_a:  ; Opcode 0x4c
shl_b:  ; Opcode 0x4d
shl_e:  ; Opcode 0x4e
shl_zpg:  ; Opcode 0x4f
shl_abs:  ; Opcode 0x50
shl_deref_x:  ; Opcode 0x51
shl_deref_y:  ; Opcode 0x52
shl_deref_e:  ; Opcode 0x53
shl_deref_sp:  ; Opcode 0x54
cmp_b_imm:  ; Opcode 0x55
cmp_b_zpg:  ; Opcode 0x56
cmp_b_abs:  ; Opcode 0x57
cmp_b_deref_x:  ; Opcode 0x58
cmp_b_deref_y:  ; Opcode 0x59
cmp_b_deref_sp:  ; Opcode 0x5a
cmp_b_a:  ; Opcode 0x5b
cmp_b_c:  ; Opcode 0x5c
cmp_b_d:  ; Opcode 0x5d
cmp_c_imm:  ; Opcode 0x5e
cmp_c_zpg:  ; Opcode 0x5f
cmp_c_abs:  ; Opcode 0x60
cmp_c_deref_x:  ; Opcode 0x61
cmp_c_deref_y:  ; Opcode 0x62
cmp_c_deref_e:  ; Opcode 0x63
cmp_c_deref_sp:  ; Opcode 0x64
cmp_c_a:  ; Opcode 0x65
cmp_c_b:  ; Opcode 0x66
cmp_c_d:  ; Opcode 0x67
cmp_d_imm:  ; Opcode 0x68
cmp_d_zpg:  ; Opcode 0x69
cmp_d_abs:  ; Opcode 0x6a
cmp_d_deref_x:  ; Opcode 0x6b
cmp_d_deref_y:  ; Opcode 0x6c
cmp_d_deref_e:  ; Opcode 0x6d
cmp_d_deref_sp:  ; Opcode 0x6e
cmp_d_a:  ; Opcode 0x6f
cmp_d_b:  ; Opcode 0x70
cmp_d_c:  ; Opcode 0x71
cmp_x_imm:  ; Opcode 0x72
cmp_x_zpg:  ; Opcode 0x73
cmp_x_abs:  ; Opcode 0x74
cmp_x_y:  ; Opcode 0x75
cmp_x_e:  ; Opcode 0x76
cmp_x_sp:  ; Opcode 0x77
cmp_x_deref_y:  ; Opcode 0x78
cmp_x_deref_e:  ; Opcode 0x79
cmp_x_deref_sp:  ; Opcode 0x7a
cmp_y_imm:  ; Opcode 0x7b
cmp_y_zpg:  ; Opcode 0x7c
cmp_y_abs:  ; Opcode 0x7d
cmp_y_x:  ; Opcode 0x7e
cmp_y_e:  ; Opcode 0x7f
cmp_y_sp:  ; Opcode 0x80
cmp_y_deref_x:  ; Opcode 0x81
cmp_y_deref_e:  ; Opcode 0x82
cmp_y_deref_sp:  ; Opcode 0x83
tst_b:  ; Opcode 0x84
tst_c:  ; Opcode 0x85
tst_d:  ; Opcode 0x86
tst_deref_x:  ; Opcode 0x87
tst_deref_y:  ; Opcode 0x88
tst_deref_sp:  ; Opcode 0x89
push_dp:  ; Opcode 0x8a
pop_dp:  ; Opcode 0x8b
jmp_abs:  ; Opcode 0x8c
jo_abs:  ; Opcode 0x8d
jno_abs:  ; Opcode 0x8e
jn_abs:  ; Opcode 0x8f
jp_abs:  ; Opcode 0x90
jz_abs:  ; Opcode 0x91
jnz_abs:  ; Opcode 0x92
jc_abs:  ; Opcode 0x93
jnc_abs:  ; Opcode 0x94
ja_abs:  ; Opcode 0x95
jna_abs:  ; Opcode 0x96
jl_abs:  ; Opcode 0x97
jl_rel:  ; Opcode 0x98
jl_ind:  ; Opcode 0x99
jge_abs:  ; Opcode 0x9a
jge_rel:  ; Opcode 0x9b
jge_ind:  ; Opcode 0x9c
jg_abs:  ; Opcode 0x9d
jg_rel:  ; Opcode 0x9e
jg_ind:  ; Opcode 0x9f
jle_abs:  ; Opcode 0xa0
jle_rel:  ; Opcode 0xa1
jle_ind:  ; Opcode 0xa2