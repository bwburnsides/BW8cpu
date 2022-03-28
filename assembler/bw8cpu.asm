#include "../instructions/opcodes.asm"

NRM_MSB = 0x00
EXT_MSB = 0x01

#fn msb(val) => val[15:8]
#fn lsb(val) => val[7:0]
#fn FALSE()  => assert(0 != 0)

#fn opcode(id) => {
    msb(id) == NRM_MSB ?
        lsb(id)
    : (msb(id) == EXT_MSB ?
        lsb(EXT) @ lsb(id)
    : (FALSE())
    )
}

#fn ASSEMBLY_TIME_CHECKS() => {
    assert(msb(EXT) == NRM_MSB)
}
_ = ASSEMBLY_TIME_CHECKS()

#ruledef bw8cpu {
    ; Housekeeping
    brk                         => opcode(BRK)
    nop                         => opcode(NOP)
    _ext                        => opcode(EXT)

    ; Flag Management
    clc                         => opcode(CLC)
    cli                         => opcode(CLI)
    clv                         => opcode(CLV)
    sec                         => opcode(SEC)
    sei                         => opcode(SEI)

    ; 8-bit Moves
    mov a, b                    => opcode(MOV_A_B)
    mov a, c                    => opcode(MOV_A_C)
    mov a, d                    => opcode(MOV_A_D)

    mov b, a                    => opcode(MOV_B_A)
    mov b, c                    => opcode(MOV_B_C)
    mov b, d                    => opcode(MOV_B_D)

    mov c, a                    => opcode(MOV_C_A)
    mov c, b                    => opcode(MOV_C_B)
    mov c, d                    => opcode(MOV_C_D)

    mov d, a                    => opcode(MOV_D_A)
    mov d, b                    => opcode(MOV_D_B)
    mov d, c                    => opcode(MOV_D_C)

    mov a, dp                   => opcode(MOV_A_DP)
    mov dp, a                   => opcode(MOV_DP_A)

    ; 8-bit Loads
    load a, #{imm: i8}          => opcode(LOAD_A_IMM)       @ imm
    load a, [{abs: u16}]        => opcode(LOAD_A_IMM)       @ abs
    load a, [{dp: u8}]          => opcode(LOAD_A_DP)        @ dp
    load a, [x]                 => opcode(LOAD_A_X)
    load a, [x + a]             => opcode(LOAD_A_X_A)
    load a, [x + b]             => opcode(LOAD_A_X_B)
    load a, [x + c]             => opcode(LOAD_A_X_C)
    load a, [x + d]             => opcode(LOAD_A_X_D)
    load a, [y]                 => opcode(LOAD_A_Y)
    load a, [y + a]             => opcode(LOAD_A_Y_A)
    load a, [y + b]             => opcode(LOAD_A_Y_B)
    load a, [y + c]             => opcode(LOAD_A_Y_C)
    load a, [y + d]             => opcode(LOAD_A_Y_D)
    load a, [sp + #{imm: u8}]   => opcode(LOAD_A_SP_IMM)    @ imm
    load a, [sp + a]            => opcode(LOAD_A_SP_A)
    load a, [sp + b]            => opcode(LOAD_A_SP_B)
    load a, [sp + c]            => opcode(LOAD_A_SP_C)
    load a, [sp + d]            => opcode(LOAD_A_SP_D)
    load a, [x + #{imm: i8}]    => asm {
        load a, #imm
        load a, [x + a]
    }
    load a, [y + #{imm: i8}]    => asm {
        load a, #imm
        load a, [y + a]
    }

    load b, #{imm: i8}          => opcode(LOAD_B_IMM)       @ imm
    load b, [{abs: u16}]        => opcode(LOAD_B_IMM)       @ abs
    load b, [{dp: u8}]          => opcode(LOAD_B_DP)        @ dp
    load b, [x]                 => opcode(LOAD_B_X)
    load b, [x + a]             => opcode(LOAD_B_X_A)
    load b, [x + b]             => opcode(LOAD_B_X_B)
    load b, [x + c]             => opcode(LOAD_B_X_C)
    load b, [x + d]             => opcode(LOAD_B_X_D)
    load b, [y]                 => opcode(LOAD_B_Y)
    load b, [y + a]             => opcode(LOAD_B_Y_A)
    load b, [y + b]             => opcode(LOAD_B_Y_B)
    load b, [y + c]             => opcode(LOAD_B_Y_C)
    load b, [y + d]             => opcode(LOAD_B_Y_D)
    load b, [sp + {imm: u8}]    => opcode(LOAD_B_SP_IMM)    @ imm
    load b, [sp + a]            => opcode(LOAD_B_SP_A)
    load b, [sp + b]            => opcode(LOAD_B_SP_B)
    load b, [sp + c]            => opcode(LOAD_B_SP_C)
    load b, [sp + d]            => opcode(LOAD_B_SP_D)
    load b, [x + #{imm: i8}]    => asm {
        load b, #imm
        load b, [x + b]
    }
    load b, [y + #{imm: i8}]    => asm {
        load b, #imm
        load b, [y + b]
    }

    load c, #{imm: i8}          => opcode(LOAD_C_IMM)       @ imm
    load c, [{abs: u16}]        => opcode(LOAD_C_IMM)       @ abs
    load c, [{dp: u8}]          => opcode(LOAD_C_DP)        @ dp
    load c, [x]                 => opcode(LOAD_C_X)
    load c, [x + a]             => opcode(LOAD_C_X_A)
    load c, [x + b]             => opcode(LOAD_C_X_B)
    load c, [x + c]             => opcode(LOAD_C_X_C)
    load c, [x + d]             => opcode(LOAD_C_X_D)
    load c, [y]                 => opcode(LOAD_C_Y)
    load c, [y + a]             => opcode(LOAD_C_Y_A)
    load c, [y + b]             => opcode(LOAD_C_Y_B)
    load c, [y + c]             => opcode(LOAD_C_Y_C)
    load c, [y + d]             => opcode(LOAD_C_Y_D)
    load c, [sp + #{imm: u8}]   => opcode(LOAD_C_SP_IMM)    @ imm
    load c, [sp + a]            => opcode(LOAD_C_SP_A)
    load c, [sp + b]            => opcode(LOAD_C_SP_B)
    load c, [sp + c]            => opcode(LOAD_C_SP_C)
    load c, [sp + d]            => opcode(LOAD_C_SP_D)
    load c, [x + #{imm: i8}]    => asm {
        load c, #imm
        load c, [x + c]
    }
    load c, [y + #{imm: i8}]    => asm {
        load c, #imm
        load c, [y + c]
    }

    load d, #{imm: i8}          => opcode(LOAD_D_IMM)       @ imm
    load d, [{abs: u16}]        => opcode(LOAD_D_IMM)       @ abs
    load d, [{dp: u8}]          => opcode(LOAD_D_DP)        @ dp
    load d, [x]                 => opcode(LOAD_D_X)
    load d, [x + a]             => opcode(LOAD_D_X_A)
    load d, [x + b]             => opcode(LOAD_D_X_B)
    load d, [x + c]             => opcode(LOAD_D_X_C)
    load d, [x + d]             => opcode(LOAD_D_X_D)
    load d, [y]                 => opcode(LOAD_D_Y)
    load d, [y + a]             => opcode(LOAD_D_Y_A)
    load d, [y + b]             => opcode(LOAD_D_Y_B)
    load d, [y + c]             => opcode(LOAD_D_Y_C)
    load d, [y + d]             => opcode(LOAD_D_Y_D)
    load d, [sp + {imm: u8}]    => opcode(LOAD_D_SP_IMM)    @ imm
    load d, [sp + a]            => opcode(LOAD_D_SP_A)
    load d, [sp + b]            => opcode(LOAD_D_SP_B)
    load d, [sp + c]            => opcode(LOAD_D_SP_C)
    load d, [sp + d]            => opcode(LOAD_D_SP_D)
    load d, [x + #{imm: i8}]    => asm {
        load d, #imm
        load d, [x + d]
    }
    load d, [y + #{imm: i8}]    => asm {
        load d, #imm
        load d, [y + d]
    }

    ; 8-bit Stores
    store a, [{abs: u16}]       => opcode(STORE_A_ABS)      @ abs
    store a, [{dp: u8}]         => opcode(STORE_A_DP)       @ dp
    store a, [x]                => opcode(STORE_A_X)
    store a, [x + a]            => opcode(STORE_A_X_A)
    store a, [x + b]            => opcode(STORE_A_X_B)
    store a, [x + c]            => opcode(STORE_A_X_C)
    store a, [x + d]            => opcode(STORE_A_X_D)
    store a, [y]                => opcode(STORE_A_Y)
    store a, [y + a]            => opcode(STORE_A_Y_A)
    store a, [y + b]            => opcode(STORE_A_Y_B)
    store a, [y + c]            => opcode(STORE_A_Y_C)
    store a, [y + d]            => opcode(STORE_A_Y_D)
    store a, [sp + {imm: u8}]   => opcode(STORE_A_SP_IMM)   @ imm
    store a, [sp + a]           => opcode(STORE_A_SP_A)
    store a, [sp + b]           => opcode(STORE_A_SP_B)
    store a, [sp + c]           => opcode(STORE_A_SP_C)
    store a, [sp + d]           => opcode(STORE_A_SP_D)

    store b, [{abs: u16}]       => opcode(STORE_B_ABS)      @ abs
    store b, [{dp: u8}]         => opcode(STORE_B_DP)       @ dp
    store b, [x]                => opcode(STORE_B_X)
    store b, [x + a]            => opcode(STORE_B_X_A)
    store b, [x + b]            => opcode(STORE_B_X_B)
    store b, [x + c]            => opcode(STORE_B_X_C)
    store b, [x + d]            => opcode(STORE_B_X_D)
    store b, [y]                => opcode(STORE_B_Y)
    store b, [y + a]            => opcode(STORE_B_Y_A)
    store b, [y + b]            => opcode(STORE_B_Y_B)
    store b, [y + c]            => opcode(STORE_B_Y_C)
    store b, [y + d]            => opcode(STORE_B_Y_D)
    store b, [sp + {imm: u8}]   => opcode(STORE_B_SP_IMM)   @ imm
    store b, [sp + a]           => opcode(STORE_B_SP_A)
    store b, [sp + b]           => opcode(STORE_B_SP_B)
    store b, [sp + c]           => opcode(STORE_B_SP_C)
    store b, [sp + d]           => opcode(STORE_B_SP_D)

    store c, [{abs: u16}]       => opcode(STORE_C_ABS)      @ abs
    store c, [{dp: u8}]         => opcode(STORE_C_DP)       @ dp
    store c, [x]                => opcode(STORE_C_X)
    store c, [x + a]            => opcode(STORE_C_X_A)
    store c, [x + b]            => opcode(STORE_C_X_B)
    store c, [x + c]            => opcode(STORE_C_X_C)
    store c, [x + d]            => opcode(STORE_C_X_D)
    store c, [y]                => opcode(STORE_C_Y)
    store c, [y + a]            => opcode(STORE_C_Y_A)
    store c, [y + b]            => opcode(STORE_C_Y_B)
    store c, [y + c]            => opcode(STORE_C_Y_C)
    store c, [y + d]            => opcode(STORE_C_Y_D)
    store c, [sp + {imm: u8}]   => opcode(STORE_C_SP_IMM)   @ imm
    store c, [sp + a]           => opcode(STORE_C_SP_A)
    store c, [sp + b]           => opcode(STORE_C_SP_B)
    store c, [sp + c]           => opcode(STORE_C_SP_C)
    store c, [sp + d]           => opcode(STORE_C_SP_D)

    store d, [{abs: u16}]       => opcode(STORE_D_ABS)      @ abs
    store d, [{dp: u8}]         => opcode(STORE_D_DP)       @ dp
    store d, [x]                => opcode(STORE_D_X)
    store d, [x + a]            => opcode(STORE_D_X_A)
    store d, [x + b]            => opcode(STORE_D_X_B)
    store d, [x + c]            => opcode(STORE_D_X_C)
    store d, [x + d]            => opcode(STORE_D_X_D)
    store d, [y]                => opcode(STORE_D_Y)
    store d, [y + a]            => opcode(STORE_D_Y_A)
    store d, [y + b]            => opcode(STORE_D_Y_B)
    store d, [y + c]            => opcode(STORE_D_Y_C)
    store d, [y + d]            => opcode(STORE_D_Y_D)
    store d, [sp + {imm: u8}]   => opcode(STORE_D_SP_IMM)   @ imm
    store d, [sp + a]           => opcode(STORE_D_SP_A)
    store d, [sp + b]           => opcode(STORE_D_SP_B)
    store d, [sp + c]           => opcode(STORE_D_SP_C)
    store d, [sp + d]           => opcode(STORE_D_SP_D)

    ; 16-bit Moves
    mov x, y                    => opcode(MOV_X_Y)
    mov x, e                    => opcode(MOV_X_E)

    mov y, x                    => opcode(MOV_Y_X)
    mov y, e                    => opcode(MOV_Y_E)

    mov e, x                    => opcode(MOV_E_X)
    mov e, y                    => opcode(MOV_E_Y)

    mov sp, e                   => opcode(MOV_SP_E)
    mov e, sp                   => opcode(MOV_E_SP)

    ; 16-bit Loads
    load x, #{imm: i16}         => opcode(LOAD_X_IMM)       @ imm
    load x, [{abs: u16}]        => opcode(LOAD_X_ABS)       @ abs
    load x, [{dp: u8}]          => opcode(LOAD_X_DP)        @ dp
    load x, [x]                 => opcode(LOAD_X_X)
    load x, [y]                 => opcode(LOAD_X_Y)
    load x, [sp + {imm: u8}]    => opcode(LOAD_X_SP_IMM)    @ imm

    load y, #{imm: i16}         => opcode(LOAD_Y_IMM)       @ imm
    load y, [{abs: u16}]        => opcode(LOAD_Y_ABS)       @ abs
    load y, [{dp: u8}]          => opcode(LOAD_Y_DP)        @ dp
    load y, [x]                 => opcode(LOAD_Y_X)
    load y, [y]                 => opcode(LOAD_Y_Y)
    load y, [sp + {imm: u8}]    => opcode(LOAD_Y_SP)        @ imm

    ; 16-bit Stores
    store x, [{abs: u16}]       => opcode(STORE_X_ABS)      @ abs
    store x, [{dp: u8}]         => opcode(STORE_X_DP)       @ dp
    store x, [x]                => opcode(STORE_X_X)
    store x, [y]                => opcode(STORE_X_Y)
    store x, [sp + {imm: u8}]   => opcode(STORE_X_SP_IMM)   @ imm

    store y, [{abs: u16}]       => opcode(STORE_Y_ABS)      @ abs
    store y, [{dp: u8}]         => opcode(STORE_Y_DP)       @ dp
    store y, [x]                => opcode(STORE_Y_X)
    store y, [y]                => opcode(STORE_Y_Y)
    store y, [sp + {imm: u8}]   => opcode(STORE_Y_SP)       @ imm

    ; Load Effective Address
    lea x, [x + a]              => opcode(LEA_X_X_A)
    lea x, [x + b]              => opcode(LEA_X_X_B)
    lea x, [x + c]              => opcode(LEA_X_X_C)
    lea x, [x + d]              => opcode(LEA_X_X_D)
    lea x, [y + a]              => opcode(LEA_X_Y_A)
    lea x, [y + b]              => opcode(LEA_X_Y_B)
    lea x, [y + c]              => opcode(LEA_X_Y_C)
    lea x, [y + d]              => opcode(LEA_X_Y_D)
    lea x, [sp + a]             => opcode(LEA_X_SP_A)
    lea x, [sp + b]             => opcode(LEA_X_SP_B)
    lea x, [sp + c]             => opcode(LEA_X_SP_C)
    lea x, [sp + d]             => opcode(LEA_X_SP_D)

    lea y, [x + a]              => opcode(LEA_Y_X_A)
    lea y, [x + b]              => opcode(LEA_Y_X_B)
    lea y, [x + c]              => opcode(LEA_Y_X_C)
    lea y, [x + d]              => opcode(LEA_Y_X_D)
    lea y, [y + a]              => opcode(LEA_Y_Y_A)
    lea y, [y + b]              => opcode(LEA_Y_Y_B)
    lea y, [y + c]              => opcode(LEA_Y_Y_C)
    lea y, [y + d]              => opcode(LEA_Y_Y_D)
    lea y, [sp + a]             => opcode(LEA_Y_SP_A)
    lea y, [sp + b]             => opcode(LEA_Y_SP_B)
    lea y, [sp + c]             => opcode(LEA_Y_SP_C)
    lea y, [sp + d]             => opcode(LEA_Y_SP_D)

    ; Add with Carry
    adc a, a                    => opcode(ADC_A_A)
    adc a, b                    => opcode(ADC_A_B)
    adc a, c                    => opcode(ADC_A_C)
    adc a, d                    => opcode(ADC_A_D)
    adc a, #{imm: i8}           => opcode(ADC_A_IMM)        @ imm
    adc a, [{dp: u8}]           => opcode(ADC_A_DP)         @ dp

    adc b, a                    => opcode(ADC_B_A)
    adc b, b                    => opcode(ADC_B_B)
    adc b, c                    => opcode(ADC_B_C)
    adc b, d                    => opcode(ADC_B_D)
    adc b, #{imm: i8}           => opcode(ADC_B_IMM)        @ imm
    adc b, [{dp: u8}]           => opcode(ADC_B_DP)         @ dp

    adc c, a                    => opcode(ADC_C_A)
    adc c, b                    => opcode(ADC_C_B)
    adc c, c                    => opcode(ADC_C_C)
    adc c, d                    => opcode(ADC_C_D)
    adc c, #{imm: i8}           => opcode(ADC_C_IMM)        @ imm
    adc c, [{dp: u8}]           => opcode(ADC_C_DP)         @ dp

    adc d, a                    => opcode(ADC_D_A)
    adc d, b                    => opcode(ADC_D_B)
    adc d, c                    => opcode(ADC_D_C)
    adc d, d                    => opcode(ADC_D_D)
    adc d, #{imm: i8}           => opcode(ADC_D_IMM)        @ imm
    adc d, [{dp: u8}]           => opcode(ADC_D_DP)         @ dp

    adc [{dp: u8}], a           => opcode(ADC_D_A)          @ dp
    adc [{dp: u8}], b           => opcode(ADC_D_B)          @ dp
    adc [{dp: u8}], c           => opcode(ADC_D_C)          @ dp
    adc [{dp: u8}], d           => opcode(ADC_D_D)          @ dp
    adc [{dp: u8}], #{imm: i8}  => opcode(ADC_D_IMM)        @ imm @ dp

    ; Add
    add a, a                    => asm {
        clc
        adc a, a
    }
    add a, b                    => asm {
        clc
        adc a, b
    }

    ; Subtract with Borrow
    sbb a, a                    => opcode(SBB_A_A)
    sbb a, b                    => opcode(SBB_A_B)
    sbb a, c                    => opcode(SBB_A_C)
    sbb a, d                    => opcode(SBB_A_D)
    sbb a, #{imm: i8}           => opcode(SBB_A_IMM)        @ imm
    sbb a, [{dp: u8}]           => opcode(SBB_A_DP)         @ dp

    sbb b, a                    => opcode(SBB_B_A)
    sbb b, b                    => opcode(SBB_B_B)
    sbb b, c                    => opcode(SBB_B_C)
    sbb b, d                    => opcode(SBB_B_D)
    sbb b, #{imm: i8}           => opcode(SBB_B_IMM)        @ imm
    sbb b, [{dp: u8}]           => opcode(SBB_B_DP)         @ dp

    sbb c, a                    => opcode(SBB_C_A)
    sbb c, b                    => opcode(SBB_C_B)
    sbb c, c                    => opcode(SBB_C_C)
    sbb c, d                    => opcode(SBB_C_D)
    sbb c, #{imm: i8}           => opcode(SBB_C_IMM)        @ imm
    sbb c, [{dp: u8}]           => opcode(SBB_C_DP)         @ dp

    sbb d, a                    => opcode(SBB_D_A)
    sbb d, b                    => opcode(SBB_D_B)
    sbb d, c                    => opcode(SBB_D_C)
    sbb d, d                    => opcode(SBB_D_D)
    sbb d, #{imm: i8}           => opcode(SBB_D_IMM)        @ imm
    sbb d, [{dp: u8}]           => opcode(SBB_D_DP)         @ dp

    sbb [{dp: u8}], a           => opcode(SBB_D_A)          @ dp
    sbb [{dp: u8}], b           => opcode(SBB_D_B)          @ dp
    sbb [{dp: u8}], c           => opcode(SBB_D_C)          @ dp
    sbb [{dp: u8}], d           => opcode(SBB_D_D)          @ dp
    sbb [{dp: u8}], #{imm: i8}  => opcode(SBB_D_IMM)        @ imm @ dp

    ; Logical AND
    and a, a                    => opcode(AND_A_A)
    and a, b                    => opcode(AND_A_B)
    and a, c                    => opcode(AND_A_C)
    and a, d                    => opcode(AND_A_D)
    and a, #{imm: i8}           => opcode(AND_A_IMM)        @ imm
    and a, [{dp: u8}]           => opcode(AND_A_DP)         @ dp

    and b, a                    => opcode(AND_B_A)
    and b, b                    => opcode(AND_B_B)
    and b, c                    => opcode(AND_B_C)
    and b, d                    => opcode(AND_B_D)
    and b, #{imm: i8}           => opcode(AND_B_IMM)        @ imm
    and b, [{dp: u8}]           => opcode(AND_B_DP)         @ dp

    and c, a                    => opcode(AND_C_A)
    and c, b                    => opcode(AND_C_B)
    and c, c                    => opcode(AND_C_C)
    and c, d                    => opcode(AND_C_D)
    and c, #{imm: i8}           => opcode(AND_C_IMM)        @ imm
    and c, [{dp: u8}]           => opcode(AND_C_DP)         @ dp

    and d, a                    => opcode(AND_D_A)
    and d, b                    => opcode(AND_D_B)
    and d, c                    => opcode(AND_D_C)
    and d, d                    => opcode(AND_D_D)
    and d, #{imm: i8}           => opcode(AND_D_IMM)        @ imm
    and d, [{dp: u8}]           => opcode(AND_D_DP)         @ dp

    and [{dp: u8}], a           => opcode(AND_D_A)          @ dp
    and [{dp: u8}], b           => opcode(AND_D_B)          @ dp
    and [{dp: u8}], c           => opcode(AND_D_C)          @ dp
    and [{dp: u8}], d           => opcode(AND_D_D)          @ dp
    and [{dp: u8}], #{imm: i8}  => opcode(AND_D_IMM)        @ imm @ dp

    ; Logical OR
    or a, a                     => opcode(OR_A_A)
    or a, b                     => opcode(OR_A_B)
    or a, c                     => opcode(OR_A_C)
    or a, d                     => opcode(OR_A_D)
    or a, #{imm: i8}            => opcode(OR_A_IMM)         @ imm
    or a, [{dp: u8}]            => opcode(OR_A_DP)          @ dp

    or b, a                     => opcode(OR_B_A)
    or b, b                     => opcode(OR_B_B)
    or b, c                     => opcode(OR_B_C)
    or b, d                     => opcode(OR_B_D)
    or b, #{imm: i8}            => opcode(OR_B_IMM)         @ imm
    or b, [{dp: u8}]            => opcode(OR_B_DP)          @ dp

    or c, a                     => opcode(OR_C_A)
    or c, b                     => opcode(OR_C_B)
    or c, c                     => opcode(OR_C_C)
    or c, d                     => opcode(OR_C_D)
    or c, #{imm: i8}            => opcode(OR_C_IMM)         @ imm
    or c, [{dp: u8}]            => opcode(OR_C_DP)          @ dp

    or d, a                     => opcode(OR_D_A)
    or d, b                     => opcode(OR_D_B)
    or d, c                     => opcode(OR_D_C)
    or d, d                     => opcode(OR_D_D)
    or d, #{imm: i8}            => opcode(OR_D_IMM)         @ imm
    or d, [{dp: u8}]            => opcode(OR_D_DP)          @ dp

    or [{dp: u8}], a            => opcode(OR_D_A)           @ dp
    or [{dp: u8}], b            => opcode(OR_D_B)           @ dp
    or [{dp: u8}], c            => opcode(OR_D_C)           @ dp
    or [{dp: u8}], d            => opcode(OR_D_D)           @ dp
    or [{dp: u8}], #{imm: i8}   => opcode(OR_D_IMM)         @ imm @ dp

    ; Logical XOR
    xor a, a                    => opcode(XOR_A_A)
    xor a, b                    => opcode(XOR_A_B)
    xor a, c                    => opcode(XOR_A_C)
    xor a, d                    => opcode(XOR_A_D)
    xor a, #{imm: i8}           => opcode(XOR_A_IMM)        @ imm
    xor a, [{dp: u8}]           => opcode(XOR_A_DP)         @ dp

    xor b, a                    => opcode(XOR_B_A)
    xor b, b                    => opcode(XOR_B_B)
    xor b, c                    => opcode(XOR_B_C)
    xor b, d                    => opcode(XOR_B_D)
    xor b, #{imm: i8}           => opcode(XOR_B_IMM)        @ imm
    xor b, [{dp: u8}]           => opcode(XOR_B_DP)         @ dp

    xor c, a                    => opcode(XOR_C_A)
    xor c, b                    => opcode(XOR_C_B)
    xor c, c                    => opcode(XOR_C_C)
    xor c, d                    => opcode(XOR_C_D)
    xor c, #{imm: i8}           => opcode(XOR_C_IMM)        @ imm
    xor c, [{dp: u8}]           => opcode(XOR_C_DP)         @ dp

    xor d, a                    => opcode(XOR_D_A)
    xor d, b                    => opcode(XOR_D_B)
    xor d, c                    => opcode(XOR_D_C)
    xor d, d                    => opcode(XOR_D_D)
    xor d, #{imm: i8}           => opcode(XOR_D_IMM)        @ imm
    xor d, [{dp: u8}]           => opcode(XOR_D_DP)         @ dp

    xor [{dp: u8}], a           => opcode(XOR_D_A)          @ dp
    xor [{dp: u8}], b           => opcode(XOR_D_B)          @ dp
    xor [{dp: u8}], c           => opcode(XOR_D_C)          @ dp
    xor [{dp: u8}], d           => opcode(XOR_D_D)          @ dp
    xor [{dp: u8}], #{imm: i8}  => opcode(XOR_D_IMM)        @ imm @ dp

    ; Logical NOT
    not a                       => opcode(NOT_A)
    not b                       => opcode(NOT_B)
    not c                       => opcode(NOT_C)
    not d                       => opcode(NOT_D)
    not [{dp: u8}]              => opcode(NOT_DP)           @ dp

    ; 2s Complement Negation
    neg a                       => opcode(NEG_A)
    neg b                       => opcode(NEG_B)
    neg c                       => opcode(NEG_C)
    neg c                       => opcode(NEG_D)
    neg [{dp: u8}]              => opcode(NEG_DP)           @ dp

    ; Shift Right with Carry
    src a                       => opcode(SRC_A)
    src b                       => opcode(SRC_B)
    src c                       => opcode(SRC_C)
    src c                       => opcode(SRC_D)
    src [{dp: u8}]              => opcode(SRC_DP)           @ dp

    ; Arithmetic Shift Right
    asr a                       => opcode(ASR_A)
    asr b                       => opcode(ASR_B)
    asr c                       => opcode(ASR_C)
    asr c                       => opcode(ASR_D)
    asr [{dp: u8}]              => opcode(ASR_DP)           @ dp

    ; Increment
    inc a                       => opcode(INC_A)
    inc b                       => opcode(INC_B)
    inc c                       => opcode(INC_C)
    inc d                       => opcode(INC_D)
    inc x                       => opcode(INC_X)
    inc y                       => opcode(INC_Y)
    inc [{dp: u8}]              => opcode(INC_DP)           @ dp

    ; Decrement
    dec a                       => opcode(DEC_A)
    dec b                       => opcode(DEC_B)
    dec c                       => opcode(DEC_C)
    dec d                       => opcode(DEC_D)
    dec x                       => opcode(DEC_X)
    dec y                       => opcode(DEC_Y)
    dec [{dp: u8}]              => opcode(DEC_DP)           @ dp

    ; Stack Pushes
    push a                      => opcode(PUSH_A)
    push b                      => opcode(PUSH_B)
    push c                      => opcode(PUSH_C)
    push d                      => opcode(PUSH_D)
    push x                      => opcode(PUSH_X)
    push y                      => opcode(PUSH_Y)
    push sr                     => opcode(PUSH_SR)

    ; Stack Pops
    pop a                       => opcode(POP_A)
    pop b                       => opcode(POP_B)
    pop c                       => opcode(POP_C)
    pop d                       => opcode(POP_D)
    pop x                       => opcode(POP_X)
    pop y                       => opcode(POP_Y)
    pop sr                      => opcode(POP_SR)

    ; Compares
    cmp a, a                    => opcode(CMP_A_A)
    cmp a, b                    => opcode(CMP_A_B)
    cmp a, c                    => opcode(CMP_A_C)
    cmp a, d                    => opcode(CMP_A_D)
    cmp a, #{imm: i8}           => opcode(CMP_A_IMM)        @ imm
    cmp a, [{dp: u8}]           => opcode(CMP_A_DP)         @ dp

    cmp b, a                    => opcode(CMP_B_A)
    cmp b, b                    => opcode(CMP_B_B)
    cmp b, c                    => opcode(CMP_B_C)
    cmp b, d                    => opcode(CMP_B_D)
    cmp b, #{imm: i8}           => opcode(CMP_B_IMM)        @ imm
    cmp b, [{dp: u8}]           => opcode(CMP_B_DP)         @ dp

    cmp c, a                    => opcode(CMP_C_A)
    cmp c, b                    => opcode(CMP_C_B)
    cmp c, c                    => opcode(CMP_C_C)
    cmp c, d                    => opcode(CMP_C_D)
    cmp c, #{imm: i8}           => opcode(CMP_C_IMM)        @ imm
    cmp c, [{dp: u8}]           => opcode(CMP_C_DP)         @ dp

    cmp d, a                    => opcode(CMP_D_A)
    cmp d, b                    => opcode(CMP_D_B)
    cmp d, c                    => opcode(CMP_D_C)
    cmp d, d                    => opcode(CMP_D_D)
    cmp d, #{imm: i8}           => opcode(CMP_D_IMM)        @ imm
    cmp d, [{dp: u8}]           => opcode(CMP_D_DP)         @ dp

    cmp [{dp: u8}], a           => opcode(CMP_DP_A)         @ dp
    cmp [{dp: u8}], b           => opcode(CMP_DP_B)         @ dp
    cmp [{dp: u8}], c           => opcode(CMP_DP_C)         @ dp
    cmp [{dp: u8}], d           => opcode(CMP_DP_D)         @ dp
    cmp [{dp: u8}], #{imm: i8}  => opcode(CMP_DP_IMM)       @ imm @ dp

    ; Tests
    tst a                       => opcode(TST_A)
    tst b                       => opcode(TST_B)
    tst c                       => opcode(TST_C)
    tst d                       => opcode(TST_D)

    ; Interrupt Control
    wai                         => opcode(WAI)
    swi [x]                     => opcode(SWI_X)
    swi [y]                     => opcode(SWI_Y)
    rti                         => opcode(RTI)

    ; Subroutine Control
    jsr {abs: u16}              => opcode(JSR_ABS)          @ abs
    jsr +{rel: u8}              => opcode(JSR_REL)          @ rel
    jsr x                       => opcode(JSR_X)
    jsr y                       => opcode(JSR_Y)
    rts                         => opcode(RTS)

    ; Unconditional Jumps
    jmp {abs: u16}              => opcode(JMP_ABS)          @ abs
    jmp +{rel: u8}              => opcode(JMP_REL)          @ rel
    jmp x                       => opcode(JMP_X)
    jmp y                       => opcode(JMP_Y)

    ; Conditional Jumps
    jo {abs: u16}               => opcode(JO_ABS)           @ abs
    jo +{rel: u8}               => opcode(JO_REL)           @ rel
    jo x                        => opcode(JO_X)
    jo y                        => opcode(JO_Y)

    jno {abs: u16}              => opcode(JNO_ABS)          @ abs
    jno +{rel: u8}              => opcode(JNO_REL)          @ rel
    jno x                       => opcode(JNO_X)
    jno y                       => opcode(JNO_Y)

    js {abs: u16}               => opcode(JS_ABS)           @ abs
    js +{rel: u8}               => opcode(JS_REL)           @ rel
    js x                        => opcode(JS_X)
    js y                        => opcode(JS_Y)

    jns {abs: u16}              => opcode(JNS_ABS)          @ abs
    jns +{rel: u8}              => opcode(JNS_REL)          @ rel
    jns x                       => opcode(JNS_X)
    jns y                       => opcode(JNS_Y)

    je {abs: u16}               => opcode(JE_ABS)           @ abs
    je +{rel: u8}               => opcode(JE_REL)           @ rel
    je x                        => opcode(JE_X)
    je y                        => opcode(JE_Y)

    jne {abs: u16}              => opcode(JNE_ABS)          @ abs
    jne +{rel: u8}              => opcode(JNE_REL)          @ rel
    jne x                       => opcode(JNE_X)
    jne y                       => opcode(JNE_Y)

    jc {abs: u16}               => opcode(JC_ABS)           @ abs
    jc +{rel: u8}               => opcode(JC_REL)           @ rel
    jc x                        => opcode(JC_X)
    jc y                        => opcode(JC_Y)

    jnc {abs: u16}              => opcode(JNC_ABS)          @ abs
    jnc +{rel: u8}              => opcode(JNC_REL)          @ rel
    jnc x                       => opcode(JNC_X)
    jnc y                       => opcode(JNC_Y)

    jbe {abs: u16}              => opcode(JBE_ABS)          @ abs
    jbe +{rel: u8}              => opcode(JBE_REL)          @ rel
    jbe x                       => opcode(JBE_X)
    jbe y                       => opcode(JBE_Y)

    ja {abs: u16}               => opcode(JA_ABS)           @ abs
    ja +{rel: u8}               => opcode(JA_REL)           @ rel
    ja x                        => opcode(JA_X)
    ja y                        => opcode(JA_Y)

    jl {abs: u16}               => opcode(JL_ABS)           @ abs
    jl +{rel: u8}               => opcode(JL_REL)           @ rel
    jl x                        => opcode(JL_X)
    jl y                        => opcode(JL_Y)

    jge {abs: u16}              => opcode(JGE_ABS)          @ abs
    jge +{rel: u8}              => opcode(JGE_REL)          @ rel
    jge x                       => opcode(JGE_X)
    jge y                       => opcode(JGE_Y)

    jle {abs: u16}              => opcode(JLE_ABS)          @ abs
    jle +{rel: u8}              => opcode(JLE_REL)          @ rel
    jle x                       => opcode(JLE_X)
    jle y                       => opcode(JLE_Y)

    jg {abs: u16}               => opcode(JG_ABS)           @ abs
    jg +{rel: u8}               => opcode(JG_REL)           @ rel
    jg x                        => opcode(JG_X)
    jg y                        => opcode(JG_Y)
}