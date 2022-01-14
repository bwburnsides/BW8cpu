#include "opcodes.asm"

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

#ruledef {
    brk         => asm{ opcode(BRK) }
    nop         => asm{ opcode(NOP) }
    wai         => asm{ opcode(WAI) }
    _ex1        => asm{ opcode(EX1) }
    _ex1        => asm{ opcode(EX2) }
    swi x       => asm{ opcode(SWI_X) }
    swi y       => asm{ opcode(SWI_Y) }

    clc         => asm { opcode(CLC) }
    cli         => asm { opcode(CLI) }
    clv         => asm { opcode(CLV) }
    sec         => asm { opcode(SEC) }
    sei         => asm { opcode(SEI) }

    mov a b     => asm{ opcode(MOV_A_B) }
    mov a c     => asm{ opcode(MOV_A_C) }
    mov a d     => asm{ opcode(MOV_A_D) }
    mov a dp    => asm{ opcode(MOV_A_DP) }

    mov b a     => asm{ opcode(MOV_B_A) }
    mov b c     => asm{ opcode(MOV_B_C) }
    mov b d     => asm{ opcode(MOV_B_D) }
    mov b dp    => asm{ opcode(MOV_B_DP) }

    mov c a     => asm{ opcode(MOV_C_A) }
    mov c b     => asm{ opcode(MOV_C_B) }
    mov c d     => asm{ opcode(MOV_C_D) }
    mov c dp    => asm{ opcode(MOV_C_DP) }

    mov d a     => asm{ opcode(MOV_D_A) }
    mov d b     => asm{ opcode(MOV_D_B) }
    mov d c     => asm{ opcode(MOV_D_C) }
    mov d dp    => asm{ opcode(MOV_D_DP) }

    mov dp a    => asm{ opcode(MOV_DP_A) }
    mov dp b    => asm{ opcode(MOV_DP_B) }
    mov dp c    => asm{ opcode(MOV_DP_C) }
    mov dp d    => asm{ opcode(MOV_DP_D) }

    mov sp x    => asm{ opcode(MOV_SP_X) }
    mov sp y    => asm{ opcode(MOV_SP_Y) }
    mov sp e    => asm{ opcode(MOV_SP_E) }

    mov x y     => asm{ opcode(MOV_X_Y) }
    mov x e     => asm{ opcode(MOV_X_E) }
    mov x sp    => asm{ opcode(MOV_X_SP) }

    mov e x     => asm{ opcode(MOV_E_X) }
    mov e y     => asm{ opcode(MOV_E_Y) }
    mov e sp    => asm{ opcode(MOV_E_SP) }

    load a #{imm: i8}
    load a {abs: i16}
    load a {zpg: i8}
    load a {zpg: i8}, a
    load a {zpg: i8}, b
    load a [x]
    load a [y]
    load a [e]
    load a [x], #{imm: i8}
    load a [y], #{imm: i8}
    load a [e], #{imm: i8}
    load a [sp], #{imm: i8}
    load a [x], a
    load a [y], a
    load a [e], a
    load a [x], b
    load a [y], b
    load a [sp], b

    add a #{imm: i8}    => asm{ opcode(ADD_A_IMM) } @ imm
}
