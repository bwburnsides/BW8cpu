#include "../instructions/opcodes.asm"

#ruledef {
    opcode({value: u16}) => {
        assert(value[15:8] == 0x00)
        value[7:0]
    }

    opcode({value: u16}) => {
        assert(value[15:8] == 0x01)
        EX1 @ value[7:0]
    }

    opcode({value: u16}) => {
        assert(value[15:8] == 0x02)
        EX2 @ value[7:0]
    }
}

#ruledef bw8cpu {
    brk                         => asm { opcode(BRK) }
    nop                         => asm { opcode(NOP) }
    wai                         => asm { opcode(WAI) }
    _ex1                        => asm { opcode(EX1) }
    _ex1                        => asm { opcode(EX2) }
    swi x                       => asm { opcode(SWI_X) }
    swi y                       => asm { opcode(SWI_Y) }

    clc                         => asm { opcode(CLC) }
    cli                         => asm { opcode(CLI) }
    clv                         => asm { opcode(CLV) }
    sec                         => asm { opcode(SEC) }
    sei                         => asm { opcode(SEI) }

    mov a, b                    => asm { opcode(MOV_A_B) }
    mov a, c                    => asm { opcode(MOV_A_C) }
    mov a, d                    => asm { opcode(MOV_A_D) }
    mov a, dp                   => asm { opcode(MOV_A_DP) }
    mov b, a                    => asm { opcode(MOV_B_A) }
    mov b, c                    => asm { opcode(MOV_B_C) }
    mov b, d                    => asm { opcode(MOV_B_D) }
    mov b, dp                   => asm { opcode(MOV_B_DP) }
    mov c, a                    => asm { opcode(MOV_C_A) }
    mov c, b                    => asm { opcode(MOV_C_B) }
    mov c, d                    => asm { opcode(MOV_C_D) }
    mov c, dp                   => asm { opcode(MOV_C_DP) }
    mov d, a                    => asm { opcode(MOV_D_A) }
    mov d, b                    => asm { opcode(MOV_D_B) }
    mov d, c                    => asm { opcode(MOV_D_C) }
    mov d, dp                   => asm { opcode(MOV_D_DP) }
    mov dp, a                   => asm { opcode(MOV_DP_A) }
    mov dp, b                   => asm { opcode(MOV_DP_B) }
    mov dp, c                   => asm { opcode(MOV_DP_C) }
    mov dp, d                   => asm { opcode(MOV_DP_D) }

    mov sp, x                   => asm { opcode(MOV_SP_X) }
    mov sp, y                   => asm { opcode(MOV_SP_Y) }
    mov sp, e                   => asm { opcode(MOV_SP_E) }
    mov x, y                    => asm { opcode(MOV_X_Y) }
    mov x, e                    => asm { opcode(MOV_X_E) }
    mov x, sp                   => asm { opcode(MOV_X_SP) }
    mov y, x                    => asm { opcode(MOV_Y_X) }
    mov y, e                    => asm { opcode(MOV_Y_E) }
    mov y, sp                   => asm { opcode(MOV_Y_SP) }
    mov e, x                    => asm { opcode(MOV_E_X) }
    mov e, y                    => asm { opcode(MOV_E_Y) }
    mov e, sp                   => asm { opcode(MOV_E_SP) }

    load a, #{imm: i8}          => asm { opcode(LOAD_A_IMM) }               @ imm
    load a, *{abs: u16}         => asm { opcode(LOAD_A_ABS) }               @ abs
    load a, *{zpg: u8}          => asm { opcode(LOAD_A_ZPG) }               @ zpg
    load a, *({zpg: u8} + a)    => asm { opcode(LOAD_A_A_INDEX_ZPG) }       @ zpg
    load a, *({zpg: u8} + b)    => asm { opcode(LOAD_A_B_INDEX_ZPG) }       @ zpg
    load a, *x                  => asm { opcode(LOAD_A_X) }
    load a, *y                  => asm { opcode(LOAD_A_Y) }
    load a, *e                  => asm { opcode(LOAD_A_E) }
    load a, *(x + #{imm: i8})   => asm { opcode(LOAD_A_CONST_INDEX_X) }     @ imm
    load a, *(y + #{imm: i8})   => asm { opcode(LOAD_A_CONST_INDEX_Y) }     @ imm
    load a, *(e + #{imm: i8})   => asm { opcode(LOAD_A_CONST_INDEX_E) }     @ imm
    load a, *(sp + #{imm: i8})  => asm { opcode(LOAD_A_CONST_INDEX_SP) }    @ imm
    load a, *(x + a)            => asm { opcode(LOAD_A_A_INDEX_X) }
    load a, *(y + a)            => asm { opcode(LOAD_A_A_INDEX_Y) }
    load a, *(e + a)            => asm { opcode(LOAD_A_A_INDEX_E) }
    load a, *(x + b)            => asm { opcode(LOAD_A_B_INDEX_X) }
    load a, *(y + b)            => asm { opcode(LOAD_A_B_INDEX_Y) }
    load a, *(sp + b)           => asm { opcode(LOAD_A_B_INDEX_SP) }

    load b, #{imm: i8}          => asm { opcode(LOAD_B_IMM) }               @ imm
    load b, *{abs: u16}         => asm { opcode(LOAD_B_ABS) }               @ abs
    load b, *{zpg: u8}          => asm { opcode(LOAD_B_ZPG) }               @ zpg
    load b, *({zpg: u8} + a)    => asm { opcode(LOAD_B_A_INDEX_ZPG) }       @ zpg
    load b, *({zpg: u8} + b)    => asm { opcode(LOAD_B_B_INDEX_ZPG) }       @ zpg
    load b, *x                  => asm { opcode(LOAD_B_X) }
    load b, *y                  => asm { opcode(LOAD_B_Y) }
    load b, *e                  => asm { opcode(LOAD_B_E) }
    load b, *(x + #{imm: i8})   => asm { opcode(LOAD_B_CONST_INDEX_X) }     @ imm
    load b, *(y + #{imm: i8})   => asm { opcode(LOAD_B_CONST_INDEX_Y) }     @ imm
    load b, *(e + #{imm: i8})   => asm { opcode(LOAD_B_CONST_INDEX_E) }     @ imm
    load b, *(sp + #{imm: i8})  => asm { opcode(LOAD_B_CONST_INDEX_SP) }    @ imm
    load b, *(x + a)            => asm { opcode(LOAD_B_A_INDEX_X) }
    load b, *(y + a)            => asm { opcode(LOAD_B_A_INDEX_Y) }
    load b, *(e + a)            => asm { opcode(LOAD_B_A_INDEX_E) }
    load b, *(x + b)            => asm { opcode(LOAD_B_B_INDEX_X) }
    load b, *(y + b)            => asm { opcode(LOAD_B_B_INDEX_Y) }
    load b, *(sp + b)           => asm { opcode(LOAD_B_B_INDEX_SP) }

    load c, #{imm: i8}          => asm { opcode(LOAD_C_IMM) }               @ imm
    load c, *{abs: u16}         => asm { opcode(LOAD_C_ABS) }               @ abs
    load c, *{zpg: u8}          => asm { opcode(LOAD_C_ZPG) }               @ zpg
    load c, *({zpg: u8} + a)    => asm { opcode(LOAD_C_A_INDEX_ZPG) }       @ zpg
    load c, *({zpg: u8} + b)    => asm { opcode(LOAD_C_B_INDEX_ZPG) }       @ zpg
    load c, *x                  => asm { opcode(LOAD_C_X) }
    load c, *y                  => asm { opcode(LOAD_C_Y) }
    load c, *e                  => asm { opcode(LOAD_C_E) }
    load c, *(x + #{imm: i8})   => asm { opcode(LOAD_C_CONST_INDEX_X) }     @ imm
    load c, *(y + #{imm: i8})   => asm { opcode(LOAD_C_CONST_INDEX_Y) }     @ imm
    load c, *(e + #{imm: i8})   => asm { opcode(LOAD_C_CONST_INDEX_E) }     @ imm
    load c, *(sp + #{imm: i8})  => asm { opcode(LOAD_C_CONST_INDEX_SP) }    @ imm
    load c, *(x + a)            => asm { opcode(LOAD_C_A_INDEX_X) }
    load c, *(y + a)            => asm { opcode(LOAD_C_A_INDEX_Y) }
    load c, *(e + a)            => asm { opcode(LOAD_C_A_INDEX_E) }
    load c, *(x + b)            => asm { opcode(LOAD_C_B_INDEX_X) }
    load c, *(y + b)            => asm { opcode(LOAD_C_B_INDEX_Y) }
    load c, *(sp + b)           => asm { opcode(LOAD_C_B_INDEX_SP) }
              
    load d, #{imm: i8}          => asm { opcode(LOAD_D_IMM) }               @ imm
    load d, *{abs: u16}         => asm { opcode(LOAD_D_ABS) }               @ abs
    load d, *{zpg: u8}          => asm { opcode(LOAD_D_ZPG) }               @ zpg
    load d, *({zpg: u8} + a)    => asm { opcode(LOAD_D_A_INDEX_ZPG) }       @ zpg
    load d, *({zpg: u8} + b)    => asm { opcode(LOAD_D_B_INDEX_ZPG) }       @ zpg
    load d, *x                  => asm { opcode(LOAD_D_X) }
    load d, *y                  => asm { opcode(LOAD_D_Y) }
    load d, *e                  => asm { opcode(LOAD_D_E) }
    load d, *(x + #{imm: i8})   => asm { opcode(LOAD_D_CONST_INDEX_X) }     @ imm
    load d, *(y + #{imm: i8})   => asm { opcode(LOAD_D_CONST_INDEX_Y) }     @ imm
    load d, *(e + #{imm: i8})   => asm { opcode(LOAD_D_CONST_INDEX_E) }     @ imm
    load d, *(sp + #{imm: i8})  => asm { opcode(LOAD_D_CONST_INDEX_SP) }    @ imm
    load d, *(x + a)            => asm { opcode(LOAD_D_A_INDEX_X) }
    load d, *(y + a)            => asm { opcode(LOAD_D_A_INDEX_Y) }
    load d, *(e + a)            => asm { opcode(LOAD_D_A_INDEX_E) }
    load d, *(x + b)            => asm { opcode(LOAD_D_B_INDEX_X) }
    load d, *(y + b)            => asm { opcode(LOAD_D_B_INDEX_Y) }
    load d, *(sp + b)           => asm { opcode(LOAD_D_B_INDEX_SP) }

    add a, #{imm: i8}           => asm{ opcode(ADD_A_IMM) }                 @ imm
}
