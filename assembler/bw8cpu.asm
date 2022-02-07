#include "../instructions/opcodes.asm"

NRM_MSB = 0x00
EX1_MSB = 0x01
EX2_MSB = 0x02

#fn msb(val) => val[15:8]
#fn lsb(val) => val[7:0]
#fn FALSE()  => assert(0 > 0)

#fn opcode(id) => {
    msb(id) == NRM_MSB ?
        lsb(id)
    : (msb(id) == EX1_MSB ?
        lsb(EX1) @ lsb(id)
    : (msb(id) == EX2_MSB ?
        lsb(EX2) @ lsb(id)
    : (FALSE())
    ))
}

#fn ASSEMBLY_TIME_CHECKS() => {
    assert(msb(EX1) == NRM_MSB)
    assert(msb(EX2) == NRM_MSB)
}
_ = ASSEMBLY_TIME_CHECKS()

#ruledef bw8cpu {
    brk                         => opcode(BRK)
    nop                         => opcode(NOP)
    wai                         => opcode(WAI)
    _ex1                        => opcode(EX1)
    _ex1                        => opcode(EX2)
    swi x                       => opcode(SWI_X)
    swi y                       => opcode(SWI_Y)

    clc                         => opcode(CLC)
    cli                         => opcode(CLI)
    clv                         => opcode(CLV)
    sec                         => opcode(SEC)
    sei                         => opcode(SEI)

    mov a, b                    => opcode(MOV_A_B)
    mov a, c                    => opcode(MOV_A_C)
    mov a, d                    => opcode(MOV_A_D)
    mov a, dp                   => opcode(MOV_A_DP)
    mov b, a                    => opcode(MOV_B_A)
    mov b, c                    => opcode(MOV_B_C)
    mov b, d                    => opcode(MOV_B_D)
    mov b, dp                   => opcode(MOV_B_DP)
    mov c, a                    => opcode(MOV_C_A)
    mov c, b                    => opcode(MOV_C_B)
    mov c, d                    => opcode(MOV_C_D)
    mov c, dp                   => opcode(MOV_C_DP)
    mov d, a                    => opcode(MOV_D_A)
    mov d, b                    => opcode(MOV_D_B)
    mov d, c                    => opcode(MOV_D_C)
    mov d, dp                   => opcode(MOV_D_DP)
    mov dp, a                   => opcode(MOV_DP_A)
    mov dp, b                   => opcode(MOV_DP_B)
    mov dp, c                   => opcode(MOV_DP_C)
    mov dp, d                   => opcode(MOV_DP_D)

    mov sp, x                   => opcode(MOV_SP_X)
    mov sp, y                   => opcode(MOV_SP_Y)
    mov sp, e                   => opcode(MOV_SP_E)
    mov x, y                    => opcode(MOV_X_Y)
    mov x, e                    => opcode(MOV_X_E)
    mov x, sp                   => opcode(MOV_X_SP)
    mov y, x                    => opcode(MOV_Y_X)
    mov y, e                    => opcode(MOV_Y_E)
    mov y, sp                   => opcode(MOV_Y_SP)
    mov e, x                    => opcode(MOV_E_X)
    mov e, y                    => opcode(MOV_E_Y)
    mov e, sp                   => opcode(MOV_E_SP)

    load a, #{imm: i8}          => opcode(LOAD_A_IMM)               @ imm
    load a, *{abs: u16}         => opcode(LOAD_A_ABS)               @ abs
    load a, *{zpg: u8}          => opcode(LOAD_A_ZPG)               @ zpg
    load a, *({zpg: u8} + a)    => opcode(LOAD_A_A_INDEX_ZPG)       @ zpg
    load a, *({zpg: u8} + b)    => opcode(LOAD_A_B_INDEX_ZPG)       @ zpg
    load a, *x                  => opcode(LOAD_A_X)
    load a, *y                  => opcode(LOAD_A_Y)
    load a, *e                  => opcode(LOAD_A_E)
    load a, *(x + #{imm: i8})   => opcode(LOAD_A_CONST_INDEX_X)     @ imm
    load a, *(y + #{imm: i8})   => opcode(LOAD_A_CONST_INDEX_Y)     @ imm
    load a, *(e + #{imm: i8})   => opcode(LOAD_A_CONST_INDEX_E)     @ imm
    load a, *(sp + #{imm: i8})  => opcode(LOAD_A_CONST_INDEX_SP)    @ imm
    load a, *(x + a)            => opcode(LOAD_A_A_INDEX_X)
    load a, *(y + a)            => opcode(LOAD_A_A_INDEX_Y)
    load a, *(e + a)            => opcode(LOAD_A_A_INDEX_E)
    load a, *(x + b)            => opcode(LOAD_A_B_INDEX_X)
    load a, *(y + b)            => opcode(LOAD_A_B_INDEX_Y)
    load a, *(sp + b)           => opcode(LOAD_A_B_INDEX_SP)

    load b, #{imm: i8}          => opcode(LOAD_B_IMM)               @ imm
    load b, *{abs: u16}         => opcode(LOAD_B_ABS)               @ abs
    load b, *{zpg: u8}          => opcode(LOAD_B_ZPG)               @ zpg
    load b, *({zpg: u8} + a)    => opcode(LOAD_B_A_INDEX_ZPG)       @ zpg
    load b, *({zpg: u8} + b)    => opcode(LOAD_B_B_INDEX_ZPG)       @ zpg
    load b, *x                  => opcode(LOAD_B_X)
    load b, *y                  => opcode(LOAD_B_Y)
    load b, *e                  => opcode(LOAD_B_E)
    load b, *(x + #{imm: i8})   => opcode(LOAD_B_CONST_INDEX_X)     @ imm
    load b, *(y + #{imm: i8})   => opcode(LOAD_B_CONST_INDEX_Y)     @ imm
    load b, *(e + #{imm: i8})   => opcode(LOAD_B_CONST_INDEX_E)     @ imm
    load b, *(sp + #{imm: i8})  => opcode(LOAD_B_CONST_INDEX_SP)    @ imm
    load b, *(x + a)            => opcode(LOAD_B_A_INDEX_X)
    load b, *(y + a)            => opcode(LOAD_B_A_INDEX_Y)
    load b, *(e + a)            => opcode(LOAD_B_A_INDEX_E)
    load b, *(x + b)            => opcode(LOAD_B_B_INDEX_X)
    load b, *(y + b)            => opcode(LOAD_B_B_INDEX_Y)
    load b, *(sp + b)           => opcode(LOAD_B_B_INDEX_SP)

    load c, #{imm: i8}          => opcode(LOAD_C_IMM)               @ imm
    load c, *{abs: u16}         => opcode(LOAD_C_ABS)               @ abs
    load c, *{zpg: u8}          => opcode(LOAD_C_ZPG)               @ zpg
    load c, *({zpg: u8} + a)    => opcode(LOAD_C_A_INDEX_ZPG)       @ zpg
    load c, *({zpg: u8} + b)    => opcode(LOAD_C_B_INDEX_ZPG)       @ zpg
    load c, *x                  => opcode(LOAD_C_X)
    load c, *y                  => opcode(LOAD_C_Y)
    load c, *e                  => opcode(LOAD_C_E)
    load c, *(x + #{imm: i8})   => opcode(LOAD_C_CONST_INDEX_X)     @ imm
    load c, *(y + #{imm: i8})   => opcode(LOAD_C_CONST_INDEX_Y)     @ imm
    load c, *(e + #{imm: i8})   => opcode(LOAD_C_CONST_INDEX_E)     @ imm
    load c, *(sp + #{imm: i8})  => opcode(LOAD_C_CONST_INDEX_SP)    @ imm
    load c, *(x + a)            => opcode(LOAD_C_A_INDEX_X)
    load c, *(y + a)            => opcode(LOAD_C_A_INDEX_Y)
    load c, *(e + a)            => opcode(LOAD_C_A_INDEX_E)
    load c, *(x + b)            => opcode(LOAD_C_B_INDEX_X)
    load c, *(y + b)            => opcode(LOAD_C_B_INDEX_Y)
    load c, *(sp + b)           => opcode(LOAD_C_B_INDEX_SP)
              
    load d, #{imm: i8}          => opcode(LOAD_D_IMM)               @ imm
    load d, *{abs: u16}         => opcode(LOAD_D_ABS)               @ abs
    load d, *{zpg: u8}          => opcode(LOAD_D_ZPG)               @ zpg
    load d, *({zpg: u8} + a)    => opcode(LOAD_D_A_INDEX_ZPG)       @ zpg
    load d, *({zpg: u8} + b)    => opcode(LOAD_D_B_INDEX_ZPG)       @ zpg
    load d, *x                  => opcode(LOAD_D_X)
    load d, *y                  => opcode(LOAD_D_Y)
    load d, *e                  => opcode(LOAD_D_E)
    load d, *(x + #{imm: i8})   => opcode(LOAD_D_CONST_INDEX_X)     @ imm
    load d, *(y + #{imm: i8})   => opcode(LOAD_D_CONST_INDEX_Y)     @ imm
    load d, *(e + #{imm: i8})   => opcode(LOAD_D_CONST_INDEX_E)     @ imm
    load d, *(sp + #{imm: i8})  => opcode(LOAD_D_CONST_INDEX_SP)    @ imm
    load d, *(x + a)            => opcode(LOAD_D_A_INDEX_X)
    load d, *(y + a)            => opcode(LOAD_D_A_INDEX_Y)
    load d, *(e + a)            => opcode(LOAD_D_A_INDEX_E)
    load d, *(x + b)            => opcode(LOAD_D_B_INDEX_X)
    load d, *(y + b)            => opcode(LOAD_D_B_INDEX_Y)
    load d, *(sp + b)           => opcode(LOAD_D_B_INDEX_SP)

    add a, #{imm: i8}           => opcode(ADD_A_IMM)                 @ imm

    xor a, a                    => opcode(XOR_A_A)
    xor a, B                    => opcode(XOR_A_B)
}
