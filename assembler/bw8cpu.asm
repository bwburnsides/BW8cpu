; NOTE: opcodes.asm is a file that can be autogenerated by opcode_assigner.py
#include "opcodes.asm"
#once
NRM_MSB = 0x00
EXT_MSB = 0x01

#fn msb(val) => val[15:8]
#fn lsb(val) => val[7:0]

#fn opcode(id) => {
    msb(id) == NRM_MSB ?
        lsb(id)
    : (msb(id) == EXT_MSB ?
        lsb(OP_EXT) @ lsb(id)
    : (assert(0 != 0))
    )
}

#fn ASSEMBLY_TIME_CHECKS() => {
    assert(msb(OP_EXT) == NRM_MSB)
}
_ = ASSEMBLY_TIME_CHECKS()

#subruledef bw8cpu_reladdr
{
	{addr: u16} =>
	{
		rel = addr - pc - 2
		assert(rel <= 127 && rel >= -128)
		rel`8
	}
}

#ruledef bw8cpu {
    ; Housekeeping
    brk                             => opcode(OP_BRK)
    nop                             => opcode(OP_NOP)
    _ext                            => opcode(OP_EXT)

    ; Flag Management
    clc                             => opcode(OP_CLC)
    cli                             => opcode(OP_CLI)
    clv                             => opcode(OP_CLV)
    sec                             => opcode(OP_SEC)
    sei                             => opcode(OP_SEI)

    ubr                             => opcode(OP_UBR)
    kbr                             => opcode(OP_KBR)

    ; IO Operations
    in a, <{port: u8}>              => opcode(OP_IN_A)          @ port
    in b, <{port: u8}>              => opcode(OP_IN_B)          @ port
    in c, <{port: u8}>              => opcode(OP_IN_C)          @ port
    in d, <{port: u8}>              => opcode(OP_IN_D)          @ port
    in [!{dp: u8}], <{port: u8}>    => opcode(OP_IN_DP)         @ dp @ port

    out <{port: u8}>, a             => opcode(OP_OUT_A)         @ port
    out <{port: u8}>, b             => opcode(OP_OUT_B)         @ port
    out <{port: u8}>, c             => opcode(OP_OUT_C)         @ port
    out <{port: u8}>, d             => opcode(OP_OUT_D)         @ port
    out <{port: u8}>, [!{dp: u8}]   => opcode(OP_OUT_DP)        @ port @ dp
    out <{port: u8}>, #{imm: i8}    => opcode(OP_OUT_IMM)       @ port @ imm

    ; 8-bit Moves
    mov a, b                        => opcode(OP_MOV_A_B)
    mov a, c                        => opcode(OP_MOV_A_C)
    mov a, d                        => opcode(OP_MOV_A_D)

    mov b, a                        => opcode(OP_MOV_B_A)
    mov b, c                        => opcode(OP_MOV_B_C)
    mov b, d                        => opcode(OP_MOV_B_D)

    mov c, a                        => opcode(OP_MOV_C_A)
    mov c, b                        => opcode(OP_MOV_C_B)
    mov c, d                        => opcode(OP_MOV_C_D)

    mov d, a                        => opcode(OP_MOV_D_A)
    mov d, b                        => opcode(OP_MOV_D_B)
    mov d, c                        => opcode(OP_MOV_D_C)

    mov a, dp                       => opcode(OP_MOV_A_DP)
    mov dp, a                       => opcode(OP_MOV_DP_A)
    mov br, a                       => opcode(OP_MOV_BR_A)
    mov a, br                       => opcode(OP_MOV_A_BR)

    ; 8-bit Loads
    load a, #{imm: i8}              => opcode(OP_LOAD_A_IMM)    @ imm
    load a, [{abs: u16}]            => opcode(OP_LOAD_A_ABS)    @ abs
    load a, [!{dp: u8}]             => opcode(OP_LOAD_A_DP)     @ dp
    load a, [x, #{idx: s8}]         => opcode(OP_LOAD_A_X_IDX)  @ idx
    load a, [x, a]                  => opcode(OP_LOAD_A_X_A)
    load a, [x, b]                  => opcode(OP_LOAD_A_X_B)
    load a, [x, c]                  => opcode(OP_LOAD_A_X_C)
    load a, [x, d]                  => opcode(OP_LOAD_A_X_D)
    load a, [y, #{idx: s8}]         => opcode(OP_LOAD_A_Y_IDX)  @ idx
    load a, [y, a]                  => opcode(OP_LOAD_A_Y_A)
    load a, [y, b]                  => opcode(OP_LOAD_A_Y_B)
    load a, [y, c]                  => opcode(OP_LOAD_A_Y_C)
    load a, [y, d]                  => opcode(OP_LOAD_A_Y_D)
    load a, [sp, #{idx: s8}]        => opcode(OP_LOAD_A_SP_IDX) @ idx
    load a, [sp, a]                 => opcode(OP_LOAD_A_SP_A)
    load a, [sp, b]                 => opcode(OP_LOAD_A_SP_B)
    load a, [sp, c]                 => opcode(OP_LOAD_A_SP_C)
    load a, [sp, d]                 => opcode(OP_LOAD_A_SP_D)

    load b, #{imm: i8}              => opcode(OP_LOAD_B_IMM)    @ imm
    load b, [{abs: u16}]            => opcode(OP_LOAD_B_ABS)    @ abs
    load b, [!{dp: u8}]             => opcode(OP_LOAD_B_DP)     @ dp
    load b, [x, #{idx: s8}]         => opcode(OP_LOAD_B_X_IDX)  @ idx
    load b, [x, a]                  => opcode(OP_LOAD_B_X_A)
    load b, [x, b]                  => opcode(OP_LOAD_B_X_B)
    load b, [x, c]                  => opcode(OP_LOAD_B_X_C)
    load b, [x, d]                  => opcode(OP_LOAD_B_X_D)
    load b, [y, #{idx: s8}]         => opcode(OP_LOAD_B_Y_IDX)  @ idx
    load b, [y, a]                  => opcode(OP_LOAD_B_Y_A)
    load b, [y, b]                  => opcode(OP_LOAD_B_Y_B)
    load b, [y, c]                  => opcode(OP_LOAD_B_Y_C)
    load b, [y, d]                  => opcode(OP_LOAD_B_Y_D)
    load b, [sp, #{idx: s8}]        => opcode(OP_LOAD_B_SP_IDX) @ idx
    load b, [sp, a]                 => opcode(OP_LOAD_B_SP_A)
    load b, [sp, b]                 => opcode(OP_LOAD_B_SP_B)
    load b, [sp, c]                 => opcode(OP_LOAD_B_SP_C)
    load b, [sp, d]                 => opcode(OP_LOAD_B_SP_D)

    load c, #{imm: i8}              => opcode(OP_LOAD_C_IMM)    @ imm
    load c, [{abs: u16}]            => opcode(OP_LOAD_C_ABS)    @ abs
    load c, [!{dp: u8}]             => opcode(OP_LOAD_C_DP)     @ dp
    load c, [x, #{idx: s8}]         => opcode(OP_LOAD_C_X_IDX)  @ idx
    load c, [x, a]                  => opcode(OP_LOAD_C_X_A)
    load c, [x, b]                  => opcode(OP_LOAD_C_X_B)
    load c, [x, c]                  => opcode(OP_LOAD_C_X_C)
    load c, [x, d]                  => opcode(OP_LOAD_C_X_D)
    load c, [y, #{idx: s8}]         => opcode(OP_LOAD_C_Y_IDX)  @ idx
    load c, [y, a]                  => opcode(OP_LOAD_C_Y_A)
    load c, [y, b]                  => opcode(OP_LOAD_C_Y_B)
    load c, [y, c]                  => opcode(OP_LOAD_C_Y_C)
    load c, [y, d]                  => opcode(OP_LOAD_C_Y_D)
    load c, [sp, #{idx: s8}]        => opcode(OP_LOAD_C_SP_IDX) @ idx
    load c, [sp, a]                 => opcode(OP_LOAD_C_SP_A)
    load c, [sp, b]                 => opcode(OP_LOAD_C_SP_B)
    load c, [sp, c]                 => opcode(OP_LOAD_C_SP_C)
    load c, [sp, d]                 => opcode(OP_LOAD_C_SP_D)

    load d, #{imm: i8}              => opcode(OP_LOAD_D_IMM)    @ imm
    load d, [{abs: u16}]            => opcode(OP_LOAD_D_ABS)    @ abs
    load d, [!{dp: u8}]             => opcode(OP_LOAD_D_DP)     @ dp
    load d, [x, #{idx: s8}]         => opcode(OP_LOAD_D_X_IDX)  @ idx
    load d, [x, a]                  => opcode(OP_LOAD_D_X_A)
    load d, [x, b]                  => opcode(OP_LOAD_D_X_B)
    load d, [x, c]                  => opcode(OP_LOAD_D_X_C)
    load d, [x, d]                  => opcode(OP_LOAD_D_X_D)
    load d, [y, #{idx: s8}]         => opcode(OP_LOAD_D_Y_IDX)  @ idx
    load d, [y, a]                  => opcode(OP_LOAD_D_Y_A)
    load d, [y, b]                  => opcode(OP_LOAD_D_Y_B)
    load d, [y, c]                  => opcode(OP_LOAD_D_Y_C)
    load d, [y, d]                  => opcode(OP_LOAD_D_Y_D)
    load d, [sp, #{idx: s8}]        => opcode(OP_LOAD_D_SP_IDX) @ idx
    load d, [sp, a]                 => opcode(OP_LOAD_D_SP_A)
    load d, [sp, b]                 => opcode(OP_LOAD_D_SP_B)
    load d, [sp, c]                 => opcode(OP_LOAD_D_SP_C)
    load d, [sp, d]                 => opcode(OP_LOAD_D_SP_D)

    ; 8-bit Stores
    store [{abs: u16}], a           => opcode(OP_STORE_A_ABS)       @ abs
    store [!{dp: u8}], a            => opcode(OP_STORE_A_DP)        @ dp
    store [x, #{idx: s8}], a        => opcode(OP_STORE_A_X_IDX)     @ idx
    store [x, a], a                 => opcode(OP_STORE_A_X_A)
    store [x, b], a                 => opcode(OP_STORE_A_X_B)
    store [x, c], a                 => opcode(OP_STORE_A_X_C)
    store [x, d], a                 => opcode(OP_STORE_A_X_D)
    store [y, #{idx: s8}], a        => opcode(OP_STORE_A_Y_IDX)     @ idx
    store [y, a], a                 => opcode(OP_STORE_A_Y_A)
    store [y, b], a                 => opcode(OP_STORE_A_Y_B)
    store [y, c], a                 => opcode(OP_STORE_A_Y_C)
    store [y, d], a                 => opcode(OP_STORE_A_Y_D)
    store [sp, #{idx: u8}], a       => opcode(OP_STORE_A_SP_IDX)    @ idx
    store [sp, a], a                => opcode(OP_STORE_A_SP_A)
    store [sp, b], a                => opcode(OP_STORE_A_SP_B)
    store [sp, c], a                => opcode(OP_STORE_A_SP_C)
    store [sp, d], a                => opcode(OP_STORE_A_SP_D)

    store [{abs: u16}], b           => opcode(OP_STORE_B_ABS)       @ abs
    store [!{dp: u8}], b            => opcode(OP_STORE_B_DP)        @ dp
    store [x, #{idx: s8}], b        => opcode(OP_STORE_B_X_IDX)     @ idx
    store [x, a], b                 => opcode(OP_STORE_B_X_A)
    store [x, b], b                 => opcode(OP_STORE_B_X_B)
    store [x, c], b                 => opcode(OP_STORE_B_X_C)
    store [x, d], b                 => opcode(OP_STORE_B_X_D)
    store [y, #{idx: s8}], b        => opcode(OP_STORE_B_Y_IDX)     @ idx
    store [y, a], b                 => opcode(OP_STORE_B_Y_A)
    store [y, b], b                 => opcode(OP_STORE_B_Y_B)
    store [y, c], b                 => opcode(OP_STORE_B_Y_C)
    store [y, d], b                 => opcode(OP_STORE_B_Y_D)
    store [sp, #{idx: s8}], b       => opcode(OP_STORE_B_SP_IDX)    @ idx
    store [sp, a], b                => opcode(OP_STORE_B_SP_A)
    store [sp, b], b                => opcode(OP_STORE_B_SP_B)
    store [sp, c], b                => opcode(OP_STORE_B_SP_C)
    store [sp, d], b                => opcode(OP_STORE_B_SP_D)

    store [{abs: u16}], c           => opcode(OP_STORE_C_ABS)       @ abs
    store [!{dp: u8}], c            => opcode(OP_STORE_C_DP)        @ dp
    store [x, #{idx: s8}], c        => opcode(OP_STORE_C_X_IDX)     @ idx
    store [x, a], c                 => opcode(OP_STORE_C_X_A)
    store [x, b], c                 => opcode(OP_STORE_C_X_B)
    store [x, c], c                 => opcode(OP_STORE_C_X_C)
    store [x, d], c                 => opcode(OP_STORE_C_X_D)
    store [y, #{idx: s8}], c        => opcode(OP_STORE_C_Y_IDX)     @ idx
    store [y, a], c                 => opcode(OP_STORE_C_Y_A)
    store [y, b], c                 => opcode(OP_STORE_C_Y_B)
    store [y, c], c                 => opcode(OP_STORE_C_Y_C)
    store [y, d], c                 => opcode(OP_STORE_C_Y_D)
    store [sp, #{idx: s8}], c       => opcode(OP_STORE_C_SP_IDX)    @ idx
    store [sp, a], c                => opcode(OP_STORE_C_SP_A)
    store [sp, b], c                => opcode(OP_STORE_C_SP_B)
    store [sp, c], c                => opcode(OP_STORE_C_SP_C)
    store [sp, d], c                => opcode(OP_STORE_C_SP_D)

    store [{abs: u16}], d           => opcode(OP_STORE_D_ABS)       @ abs
    store [!{dp: u8}], d            => opcode(OP_STORE_D_DP)        @ dp
    store [x, #{idx: s8}], d        => opcode(OP_STORE_D_X_IDX)     @ idx
    store [x, a], d                 => opcode(OP_STORE_D_X_A)
    store [x, b], d                 => opcode(OP_STORE_D_X_B)
    store [x, c], d                 => opcode(OP_STORE_D_X_C)
    store [x, d], d                 => opcode(OP_STORE_D_X_D)
    store [y, #{idx: s8}], d        => opcode(OP_STORE_D_Y_IDX)     @ idx
    store [y, a], d                 => opcode(OP_STORE_D_Y_A)
    store [y, b], d                 => opcode(OP_STORE_D_Y_B)
    store [y, c], d                 => opcode(OP_STORE_D_Y_C)
    store [y, d], d                 => opcode(OP_STORE_D_Y_D)
    store [sp, #{idx: s8}], d       => opcode(OP_STORE_D_SP_IDX)    @ idx
    store [sp, a], d                => opcode(OP_STORE_D_SP_A)
    store [sp, b], d                => opcode(OP_STORE_D_SP_B)
    store [sp, c], d                => opcode(OP_STORE_D_SP_C)
    store [sp, d], d                => opcode(OP_STORE_D_SP_D)

    ; 16-bit Moves
    mov x, y                        => opcode(OP_MOV_X_Y)
    mov x, ab                       => opcode(OP_MOV_X_AB)
    mov x, cd                       => opcode(OP_MOV_X_CD)

    mov y, x                        => opcode(OP_MOV_Y_X)
    mov y, ab                       => opcode(OP_MOV_Y_AB)
    mov y, cd                       => opcode(OP_MOV_Y_CD)

    mov ab, x                       => opcode(OP_MOV_AB_X)
    mov ab, y                       => opcode(OP_MOV_AB_Y)

    mov cd, x                       => opcode(OP_MOV_CD_X)
    mov cd, y                       => opcode(OP_MOV_CD_Y)

    mov sp, x                       => opcode(OP_MOV_SP_X)
    mov x, sp                       => opcode(OP_MOV_X_SP)

    ; 16-bit Loads
    load x, #{imm: i16}             => opcode(OP_LOAD_X_IMM)    @ imm
    load x, [{abs: u16}]            => opcode(OP_LOAD_X_ABS)    @ abs
    load x, [!{dp: u8}]             => opcode(OP_LOAD_X_DP)     @ dp
    load x, [x, #{idx: s8}]         => opcode(OP_LOAD_X_X_IDX)  @ idx
    load x, [y, #{idx: s8}]         => opcode(OP_LOAD_X_Y_IDX)  @ idx
    load x, [sp, #{idx: s8}]        => opcode(OP_LOAD_X_SP_IDX) @ idx

    load y, #{imm: i16}             => opcode(OP_LOAD_Y_IMM)    @ imm
    load y, [{abs: u16}]            => opcode(OP_LOAD_Y_ABS)    @ abs
    load y, [!{dp: u8}]             => opcode(OP_LOAD_Y_DP)     @ dp
    load y, [x, #{idx: s8}]         => opcode(OP_LOAD_Y_X_IDX)  @ idx
    load y, [y, #{idx: s8}]         => opcode(OP_LOAD_Y_Y_IDX)  @ idx
    load y, [sp, #{idx: u8}]        => opcode(OP_LOAD_Y_SP_IDX) @ idx

    ; 16-bit Stores
    store [{abs: u16}], x           => opcode(OP_STORE_X_ABS)       @ abs
    store [!{dp: u8}], x            => opcode(OP_STORE_X_DP)        @ dp
    store [x, #{idx: s8}], x        => opcode(OP_STORE_X_X_IDX)     @ idx
    store [y, #{idx: s8}], x        => opcode(OP_STORE_X_Y_IDX)     @ idx
    store [sp, #{idx: u8}], x       => opcode(OP_STORE_X_SP_IDX)    @ idx

    store [{abs: u16}], y           => opcode(OP_STORE_Y_ABS)       @ abs
    store [!{dp: u8}], y            => opcode(OP_STORE_Y_DP)        @ dp
    store [x, #{idx: s8}], y        => opcode(OP_STORE_Y_X_IDX)     @ idx
    store [y, #{idx: s8}], y        => opcode(OP_STORE_Y_Y_IDX)     @ idx
    store [sp, #{imm: u8}], y       => opcode(OP_STORE_Y_SP_IDX)    @ idx

    ; Load Effective Address
    lea x, #{idx: s8}               => opcode(OP_LEA_X_IDX)         @ idx
    lea x, a                        => opcode(OP_LEA_X_A)
    lea x, b                        => opcode(OP_LEA_X_B)
    lea x, c                        => opcode(OP_LEA_X_C)
    lea x, d                        => opcode(OP_LEA_X_D)
    lea y, #{idx: s8}               => opcode(OP_LEA_Y_IDX)         @ idx
    lea y, a                        => opcode(OP_LEA_Y_A)
    lea y, b                        => opcode(OP_LEA_Y_B)
    lea y, c                        => opcode(OP_LEA_Y_C)
    lea y, d                        => opcode(OP_LEA_Y_D)
    lea sp, #{idx: s8}              => opcode(OP_LEA_SP_IDX)        @ idx
    lea sp, a                       => opcode(OP_LEA_SP_A)
    lea sp, b                       => opcode(OP_LEA_SP_B)
    lea sp, c                       => opcode(OP_LEA_SP_C)
    lea sp, d                       => opcode(OP_LEA_SP_D)

    ; Add with Carry
    adc a, a                        => opcode(OP_ADC_A_A)
    adc a, b                        => opcode(OP_ADC_A_B)
    adc a, c                        => opcode(OP_ADC_A_C)
    adc a, d                        => opcode(OP_ADC_A_D)
    adc a, #{imm: i8}               => opcode(OP_ADC_A_IMM) @ imm
    adc a, [!{dp: u8}]              => opcode(OP_ADC_A_DP)  @ dp

    adc b, a                        => opcode(OP_ADC_B_A)
    adc b, b                        => opcode(OP_ADC_B_B)
    adc b, c                        => opcode(OP_ADC_B_C)
    adc b, d                        => opcode(OP_ADC_B_D)
    adc b, #{imm: i8}               => opcode(OP_ADC_B_IMM) @ imm
    adc b, [!{dp: u8}]              => opcode(OP_ADC_B_DP)  @ dp

    adc c, a                        => opcode(OP_ADC_C_A)
    adc c, b                        => opcode(OP_ADC_C_B)
    adc c, c                        => opcode(OP_ADC_C_C)
    adc c, d                        => opcode(OP_ADC_C_D)
    adc c, #{imm: i8}               => opcode(OP_ADC_C_IMM) @ imm
    adc c, [!{dp: u8}]              => opcode(OP_ADC_C_DP)  @ dp

    adc d, a                        => opcode(OP_ADC_D_A)
    adc d, b                        => opcode(OP_ADC_D_B)
    adc d, c                        => opcode(OP_ADC_D_C)
    adc d, d                        => opcode(OP_ADC_D_D)
    adc d, #{imm: i8}               => opcode(OP_ADC_D_IMM) @ imm
    adc d, [!{dp: u8}]              => opcode(OP_ADC_D_DP)  @ dp

    adc [!{dp: u8}], a              => opcode(OP_ADC_D_A)   @ dp
    adc [!{dp: u8}], b              => opcode(OP_ADC_D_B)   @ dp
    adc [!{dp: u8}], c              => opcode(OP_ADC_D_C)   @ dp
    adc [!{dp: u8}], d              => opcode(OP_ADC_D_D)   @ dp
    adc [!{dp: u8}], #{imm: i8}     => opcode(OP_ADC_D_IMM) @ imm @ dp

    ; Subtract with Carry
    sbc a, a                        => opcode(OP_SBC_A_A)
    sbc a, b                        => opcode(OP_SBC_A_B)
    sbc a, c                        => opcode(OP_SBC_A_C)
    sbc a, d                        => opcode(OP_SBC_A_D)
    sbc a, #{imm: i8}               => opcode(OP_SBC_A_IMM) @ imm
    sbc a, [!{dp: u8}]              => opcode(OP_SBC_A_DP)  @ dp

    sbc b, a                        => opcode(OP_SBC_B_A)
    sbc b, b                        => opcode(OP_SBC_B_B)
    sbc b, c                        => opcode(OP_SBC_B_C)
    sbc b, d                        => opcode(OP_SBC_B_D)
    sbc b, #{imm: i8}               => opcode(OP_SBC_B_IMM) @ imm
    sbc b, [!{dp: u8}]              => opcode(OP_SBC_B_DP)  @ dp

    sbc c, a                        => opcode(OP_SBC_C_A)
    sbc c, b                        => opcode(OP_SBC_C_B)
    sbc c, c                        => opcode(OP_SBC_C_C)
    sbc c, d                        => opcode(OP_SBC_C_D)
    sbc c, #{imm: i8}               => opcode(OP_SBC_C_IMM) @ imm
    sbc c, [!{dp: u8}]              => opcode(OP_SBC_C_DP)  @ dp

    sbc d, a                        => opcode(OP_SBC_D_A)
    sbc d, b                        => opcode(OP_SBC_D_B)
    sbc d, c                        => opcode(OP_SBC_D_C)
    sbc d, d                        => opcode(OP_SBC_D_D)
    sbc d, #{imm: i8}               => opcode(OP_SBC_D_IMM) @ imm
    sbc d, [!{dp: u8}]              => opcode(OP_SBC_D_DP)  @ dp

    sbc [!{dp: u8}], a              => opcode(OP_SBC_D_A)   @ dp
    sbc [!{dp: u8}], b              => opcode(OP_SBC_D_B)   @ dp
    sbc [!{dp: u8}], c              => opcode(OP_SBC_D_C)   @ dp
    sbc [!{dp: u8}], d              => opcode(OP_SBC_D_D)   @ dp
    sbc [!{dp: u8}], #{imm: i8}     => opcode(OP_SBC_D_IMM) @ imm @ dp

    ; Logical AND
    and a, b                        => opcode(OP_AND_A_B)
    and a, c                        => opcode(OP_AND_A_C)
    and a, d                        => opcode(OP_AND_A_D)
    and a, #{imm: i8}               => opcode(OP_AND_A_IMM) @ imm
    and a, [!{dp: u8}]              => opcode(OP_AND_A_DP)  @ dp

    and b, a                        => opcode(OP_AND_B_A)
    and b, c                        => opcode(OP_AND_B_C)
    and b, d                        => opcode(OP_AND_B_D)
    and b, #{imm: i8}               => opcode(OP_AND_B_IMM) @ imm
    and b, [!{dp: u8}]              => opcode(OP_AND_B_DP)  @ dp

    and c, a                        => opcode(OP_AND_C_A)
    and c, b                        => opcode(OP_AND_C_B)
    and c, d                        => opcode(OP_AND_C_D)
    and c, #{imm: i8}               => opcode(OP_AND_C_IMM) @ imm
    and c, [!{dp: u8}]              => opcode(OP_AND_C_DP)  @ dp

    and d, a                        => opcode(OP_AND_D_A)
    and d, b                        => opcode(OP_AND_D_B)
    and d, c                        => opcode(OP_AND_D_C)
    and d, #{imm: i8}               => opcode(OP_AND_D_IMM) @ imm
    and d, [!{dp: u8}]              => opcode(OP_AND_D_DP)  @ dp

    and [!{dp: u8}], a              => opcode(OP_AND_D_A)   @ dp
    and [!{dp: u8}], b              => opcode(OP_AND_D_B)   @ dp
    and [!{dp: u8}], c              => opcode(OP_AND_D_C)   @ dp
    and [!{dp: u8}], d              => opcode(OP_AND_D_D)   @ dp
    and [!{dp: u8}], #{imm: i8}     => opcode(OP_AND_D_IMM) @ imm @ dp

    ; Logical OR
    or a, b                         => opcode(OP_OR_A_B)
    or a, c                         => opcode(OP_OR_A_C)
    or a, d                         => opcode(OP_OR_A_D)
    or a, #{imm: i8}                => opcode(OP_OR_A_IMM)  @ imm
    or a, [!{dp: u8}]               => opcode(OP_OR_A_DP)   @ dp

    or b, a                         => opcode(OP_OR_B_A)
    or b, c                         => opcode(OP_OR_B_C)
    or b, d                         => opcode(OP_OR_B_D)
    or b, #{imm: i8}                => opcode(OP_OR_B_IMM)  @ imm
    or b, [!{dp: u8}]               => opcode(OP_OR_B_DP)   @ dp

    or c, a                         => opcode(OP_OR_C_A)
    or c, b                         => opcode(OP_OR_C_B)
    or c, d                         => opcode(OP_OR_C_D)
    or c, #{imm: i8}                => opcode(OP_OR_C_IMM)  @ imm
    or c, [!{dp: u8}]               => opcode(OP_OR_C_DP)   @ dp

    or d, a                         => opcode(OP_OR_D_A)
    or d, b                         => opcode(OP_OR_D_B)
    or d, c                         => opcode(OP_OR_D_C)
    or d, #{imm: i8}                => opcode(OP_OR_D_IMM)  @ imm
    or d, [!{dp: u8}]               => opcode(OP_OR_D_DP)   @ dp

    or [!{dp: u8}], a               => opcode(OP_OR_D_A)    @ dp
    or [!{dp: u8}], b               => opcode(OP_OR_D_B)    @ dp
    or [!{dp: u8}], c               => opcode(OP_OR_D_C)    @ dp
    or [!{dp: u8}], d               => opcode(OP_OR_D_D)    @ dp
    or [!{dp: u8}], #{imm: i8}      => opcode(OP_OR_D_IMM)  @ imm @ dp

    ; Logical XOR
    xor a, a                        => opcode(OP_XOR_A_A)
    xor a, b                        => opcode(OP_XOR_A_B)
    xor a, c                        => opcode(OP_XOR_A_C)
    xor a, d                        => opcode(OP_XOR_A_D)
    xor a, #{imm: i8}               => opcode(OP_XOR_A_IMM) @ imm
    xor a, [!{dp: u8}]              => opcode(OP_XOR_A_DP)  @ dp

    xor b, a                        => opcode(OP_XOR_B_A)
    xor b, b                        => opcode(OP_XOR_B_B)
    xor b, c                        => opcode(OP_XOR_B_C)
    xor b, d                        => opcode(OP_XOR_B_D)
    xor b, #{imm: i8}               => opcode(OP_XOR_B_IMM) @ imm
    xor b, [!{dp: u8}]              => opcode(OP_XOR_B_DP)  @ dp

    xor c, a                        => opcode(OP_XOR_C_A)
    xor c, b                        => opcode(OP_XOR_C_B)
    xor c, c                        => opcode(OP_XOR_C_C)
    xor c, d                        => opcode(OP_XOR_C_D)
    xor c, #{imm: i8}               => opcode(OP_XOR_C_IMM) @ imm
    xor c, [!{dp: u8}]              => opcode(OP_XOR_C_DP)  @ dp

    xor d, a                        => opcode(OP_XOR_D_A)
    xor d, b                        => opcode(OP_XOR_D_B)
    xor d, c                        => opcode(OP_XOR_D_C)
    xor d, d                        => opcode(OP_XOR_D_D)
    xor d, #{imm: i8}               => opcode(OP_XOR_D_IMM) @ imm
    xor d, [!{dp: u8}]              => opcode(OP_XOR_D_DP)  @ dp

    xor [!{dp: u8}], a              => opcode(OP_XOR_D_A)   @ dp
    xor [!{dp: u8}], b              => opcode(OP_XOR_D_B)   @ dp
    xor [!{dp: u8}], c              => opcode(OP_XOR_D_C)   @ dp
    xor [!{dp: u8}], d              => opcode(OP_XOR_D_D)   @ dp
    xor [!{dp: u8}], #{imm: i8}     => opcode(OP_XOR_D_IMM) @ imm @ dp

    ; Logical NOT
    not a                       => opcode(OP_NOT_A)
    not b                       => opcode(OP_NOT_B)
    not c                       => opcode(OP_NOT_C)
    not d                       => opcode(OP_NOT_D)
    not [!{dp: u8}]             => opcode(OP_NOT_DP)    @ dp

    ; 2s Complement Negation
    neg a                       => opcode(OP_NEG_A)
    neg b                       => opcode(OP_NEG_B)
    neg c                       => opcode(OP_NEG_C)
    neg c                       => opcode(OP_NEG_D)
    neg [!{dp: u8}]             => opcode(OP_NEG_DP)    @ dp

    ; Shift Right with Carry
    src a                       => opcode(OP_SRC_A)
    src b                       => opcode(OP_SRC_B)
    src c                       => opcode(OP_SRC_C)
    src d                       => opcode(OP_SRC_D)
    src [!{dp: u8}]             => opcode(OP_SRC_DP)    @ dp

    ; Arithmetic Shift Right
    asr a                       => opcode(OP_ASR_A)
    asr b                       => opcode(OP_ASR_B)
    asr c                       => opcode(OP_ASR_C)
    asr c                       => opcode(OP_ASR_D)
    asr [!{dp: u8}]             => opcode(OP_ASR_DP)    @ dp

    ; Increment
    inc a                       => opcode(OP_INC_A)
    inc b                       => opcode(OP_INC_B)
    inc c                       => opcode(OP_INC_C)
    inc d                       => opcode(OP_INC_D)
    inc x                       => opcode(OP_INC_X)
    inc y                       => opcode(OP_INC_Y)
    inc [!{dp: u8}]             => opcode(OP_INC_DP)    @ dp

    ; Decrement
    dec a                       => opcode(OP_DEC_A)
    dec b                       => opcode(OP_DEC_B)
    dec c                       => opcode(OP_DEC_C)
    dec d                       => opcode(OP_DEC_D)
    dec x                       => opcode(OP_DEC_X)
    dec y                       => opcode(OP_DEC_Y)
    dec [!{dp: u8}]             => opcode(OP_DEC_DP)    @ dp

    ; Stack Pushes
    push a                      => opcode(OP_PUSH_A)
    push b                      => opcode(OP_PUSH_B)
    push c                      => opcode(OP_PUSH_C)
    push d                      => opcode(OP_PUSH_D)
    push x                      => opcode(OP_PUSH_X)
    push y                      => opcode(OP_PUSH_Y)
    push sr                     => opcode(OP_PUSH_SR)

    ; Stack Pops
    pop a                       => opcode(OP_POP_A)
    pop b                       => opcode(OP_POP_B)
    pop c                       => opcode(OP_POP_C)
    pop d                       => opcode(OP_POP_D)
    pop x                       => opcode(OP_POP_X)
    pop y                       => opcode(OP_POP_Y)
    pop sr                      => opcode(OP_POP_SR)

    ; Compares
    cmp a, a                    => opcode(OP_CMP_A_A)
    cmp a, b                    => opcode(OP_CMP_A_B)
    cmp a, c                    => opcode(OP_CMP_A_C)
    cmp a, d                    => opcode(OP_CMP_A_D)
    cmp a, #{imm: i8}           => opcode(OP_CMP_A_IMM)     @ imm
    cmp a, [!{dp: u8}]          => opcode(OP_CMP_A_DP)      @ dp

    cmp b, a                    => opcode(OP_CMP_B_A)
    cmp b, b                    => opcode(OP_CMP_B_B)
    cmp b, c                    => opcode(OP_CMP_B_C)
    cmp b, d                    => opcode(OP_CMP_B_D)
    cmp b, #{imm: i8}           => opcode(OP_CMP_B_IMM)     @ imm
    cmp b, [!{dp: u8}]          => opcode(OP_CMP_B_DP)      @ dp

    cmp c, a                    => opcode(OP_CMP_C_A)
    cmp c, b                    => opcode(OP_CMP_C_B)
    cmp c, c                    => opcode(OP_CMP_C_C)
    cmp c, d                    => opcode(OP_CMP_C_D)
    cmp c, #{imm: i8}           => opcode(OP_CMP_C_IMM)     @ imm
    cmp c, [!{dp: u8}]          => opcode(OP_CMP_C_DP)      @ dp

    cmp d, a                    => opcode(OP_CMP_D_A)
    cmp d, b                    => opcode(OP_CMP_D_B)
    cmp d, c                    => opcode(OP_CMP_D_C)
    cmp d, d                    => opcode(OP_CMP_D_D)
    cmp d, #{imm: i8}           => opcode(OP_CMP_D_IMM)     @ imm
    cmp d, [!{dp: u8}]          => opcode(OP_CMP_D_DP)      @ dp

    cmp [!{dp: u8}], a          => opcode(OP_CMP_DP_A)      @ dp
    cmp [!{dp: u8}], b          => opcode(OP_CMP_DP_B)      @ dp
    cmp [!{dp: u8}], c          => opcode(OP_CMP_DP_C)      @ dp
    cmp [!{dp: u8}], d          => opcode(OP_CMP_DP_D)      @ dp
    cmp [!{dp: u8}], #{imm: i8} => opcode(OP_CMP_DP_IMM)    @ dp @ imm

    ; Tests
    tst a                       => opcode(OP_TST_A)
    tst b                       => opcode(OP_TST_B)
    tst c                       => opcode(OP_TST_C)
    tst d                       => opcode(OP_TST_D)
    tst [!{dp: u8}]             => opcode(OP_TST_DP)        @ dp

    ; Subroutine Control
    jsr {abs: u16}              => opcode(OP_JSR_ABS)          @ abs
    jsr {rel: bw8cpu_reladdr}   => opcode(OP_JSR_REL)          @ rel
    jsr x                       => opcode(OP_JSR_X)
    jsr y                       => opcode(OP_JSR_Y)
    rts                         => opcode(OP_RTS)
    rti                         => opcode(OP_RTI)

    ; Unconditional Jumps
    jmp_abs {abs: u16}          => opcode(OP_JMP_ABS)          @ abs
    jmp {abs: u16}              => opcode(OP_JMP_ABS)          @ abs
    jmp {rel: bw8cpu_reladdr}   => opcode(OP_JMP_REL)          @ rel
    jmp x                       => opcode(OP_JMP_X)
    jmp y                       => opcode(OP_JMP_Y)

    ; Conditional Jumps
    jo {abs: u16}               => opcode(OP_JO_ABS)           @ abs
    jo {rel: bw8cpu_reladdr}    => opcode(OP_JO_REL)           @ rel
    jo x                        => opcode(OP_JO_X)
    jo y                        => opcode(OP_JO_Y)

    jno {abs: u16}              => opcode(OP_JNO_ABS)          @ abs
    jno {rel: bw8cpu_reladdr}   => opcode(OP_JNO_REL)          @ rel
    jno x                       => opcode(OP_JNO_X)
    jno y                       => opcode(OP_JNO_Y)

    js {abs: u16}               => opcode(OP_JS_ABS)           @ abs
    js {rel: bw8cpu_reladdr}    => opcode(OP_JS_REL)           @ rel
    js x                        => opcode(OP_JS_X)
    js y                        => opcode(OP_JS_Y)

    jns {abs: u16}              => opcode(OP_JNS_ABS)          @ abs
    jns {rel: bw8cpu_reladdr}   => opcode(OP_JNS_REL)          @ rel
    jns x                       => opcode(OP_JNS_X)
    jns y                       => opcode(OP_JNS_Y)

    je {abs: u16}               => opcode(OP_JE_ABS)           @ abs
    je {rel: bw8cpu_reladdr}    => opcode(OP_JE_REL)           @ rel
    je x                        => opcode(OP_JE_X)
    je y                        => opcode(OP_JE_Y)

    jne {abs: u16}              => opcode(OP_JNE_ABS)          @ abs
    jne {rel: bw8cpu_reladdr}   => opcode(OP_JNE_REL)          @ rel
    jne x                       => opcode(OP_JNE_X)
    jne y                       => opcode(OP_JNE_Y)

    jc {abs: u16}               => opcode(OP_JC_ABS)           @ abs
    jc {rel: bw8cpu_reladdr}    => opcode(OP_JC_REL)           @ rel
    jc x                        => opcode(OP_JC_X)
    jc y                        => opcode(OP_JC_Y)

    jnc {abs: u16}              => opcode(OP_JNC_ABS)          @ abs
    jnc {rel: bw8cpu_reladdr}   => opcode(OP_JNC_REL)          @ rel
    jnc x                       => opcode(OP_JNC_X)
    jnc y                       => opcode(OP_JNC_Y)

    jbe {abs: u16}              => opcode(OP_JBE_ABS)          @ abs
    jbe {rel: bw8cpu_reladdr}   => opcode(OP_JBE_REL)          @ rel
    jbe x                       => opcode(OP_JBE_X)
    jbe y                       => opcode(OP_JBE_Y)

    ja {abs: u16}               => opcode(OP_JA_ABS)           @ abs
    ja {rel: bw8cpu_reladdr}    => opcode(OP_JA_REL)           @ rel
    ja x                        => opcode(OP_JA_X)
    ja y                        => opcode(OP_JA_Y)

    jl {abs: u16}               => opcode(OP_JL_ABS)           @ abs
    jl {rel: bw8cpu_reladdr}    => opcode(OP_JL_REL)           @ rel
    jl x                        => opcode(OP_JL_X)
    jl y                        => opcode(OP_JL_Y)

    jge {abs: u16}              => opcode(OP_JGE_ABS)          @ abs
    jge {rel: bw8cpu_reladdr}   => opcode(OP_JGE_REL)          @ rel
    jge x                       => opcode(OP_JGE_X)
    jge y                       => opcode(OP_JGE_Y)

    jle {abs: u16}              => opcode(OP_JLE_ABS)          @ abs
    jle {rel: bw8cpu_reladdr}   => opcode(OP_JLE_REL)          @ rel
    jle x                       => opcode(OP_JLE_X)
    jle y                       => opcode(OP_JLE_Y)

    jg {abs: u16}               => opcode(OP_JG_ABS)           @ abs
    jg {rel: bw8cpu_reladdr}    => opcode(OP_JG_REL)           @ rel
    jg x                        => opcode(OP_JG_X)
    jg y                        => opcode(OP_JG_Y)
}

#ruledef bw8cpu_aliases {
    load a, [x]     => asm{load a, [x, #0]}
    load a, [y]     => asm{load a, [y, #0]}
    load b, [x]     => asm{load b, [x, #0]}
    load b, [y]     => asm{load b, [y, #0]}
    load c, [x]     => asm{load c, [x, #0]}
    load c, [y]     => asm{load c, [y, #0]}
    load d, [x]     => asm{load d, [x, #0]}
    load d, [y]     => asm{load d, [y, #0]}

    store a, [x]    => asm{store a, [x, #0]}
    store a, [y]    => asm{store a, [y, #0]}
    store b, [x]    => asm{store b, [x, #0]}
    store b, [y]    => asm{store b, [y, #0]}
    store c, [x]    => asm{store c, [x, #0]}
    store c, [y]    => asm{store c, [y, #0]}
    store d, [x]    => asm{store d, [x, #0]}
    store d, [y]    => asm{store d, [y, #0]}

    load x, [x]     => asm{load x, [x, #0]}
    load x, [y]     => asm{load x, [y, #0]}
    load y, [x]     => asm{load y, [x, #0]}
    load y, [y]     => asm{load y, [y, #0]}

    load ab, #{imm: i16}    => asm{
        load a, #imm[15:8]
        load b, #imm[7:0]
    }
    load cd, #{imm: i16}    => asm{
        load c, #imm[15:8]
        load d, #imm[7:0]
    }

    store x, [x]    => asm{store x, [x, #0]}
    store x, [y]    => asm{store x, [y, #0]}
    store y, [x]    => asm{store y, [x, #0]}
    store y, [y]    => asm{store y, [y, #0]}

    mov ab, cd  => asm{
        mov a, c
        mov b, d
    }
    mov cd, ab  => asm{
        mov c, a
        mov d, b
    }

    swap a, b   => asm{
        xor a, b
        xor b, a
        xor a, b
    }
    swap b, a   => asm{swap a, b}

    swap a, c   => asm{
        xor a, c
        xor c, a
        xor a, c
    }
    swap c, a   => asm{swap a, c}

    swap a, d   => asm{
        xor a, d
        xor d, a
        xor a, d
    }
    swap d, a   => asm{swap a, d}

    swap b, c   => asm{
        xor b, c
        xor c, b
        xor b, c
    }
    swap c, b   => asm{swap b, c}

    swap b, d   => asm{
        xor b, d
        xor d, b
        xor b, d
    }
    swap d, b   => asm{swap b, d}

    swap c, d   => asm{
        xor c, d
        xor d, c
        xor c, d
    }
    swap d, c   => asm{swap c, d}

    clr a       => asm{xor a, a}
    clr b       => asm{xor b, b}
    clr c       => asm{xor c, c}
    clr d       => asm{xor d, d}

    push ab     => asm{
        push a
        push b
    }
    push cd     => asm{
        push c
        push d
    }

    pop ab      => asm{
        pop b
        pop a
    }

    pop cd      => asm{
        pop d
        pop c
    }

    swi [x]     => asm{
        sei
        push sr
        load x, [x]
        jsr x
    }
    swi [y]     => asm{
        sei
        push sr
        load y, [y]
        jsr y
    }

    add a, a => asm{
        clc
        adc a, a
    }
    add a, b => asm{
        clc
        adc a, b
    }
    add a, c => asm{
        clc
        adc a, c
    }
    add a, d => asm{
        clc
        adc a, d
    }
    add a, #{imm: i8} => asm{
        clc
        adc a, #imm
    }
    add a, [!{dp: u8}] => asm{
        clc
        adc a, [!dp]
    }
    add b, a => asm{
        clc
        adc b, a
    }
    add b, b => asm{
        clc
        adc b, b
    }
    add b, c => asm{
        clc
        adc b, c
    }
    add b, d => asm{
        clc
        adc b, d
    }
    add b, #{imm: i8} => asm{
        clc
        adc b, #imm
    }
    add b, [!{dp: u8}] => asm{
        clc
        adc b, [!dp]
    }
    add c, a => asm{
        clc
        adc c, a
    }
    add c, b => asm{
        clc
        adc c, b
    }
    add c, c => asm{
        clc
        adc c, c
    }
    add c, d => asm{
        clc
        adc c, d
    }
    add c, #{imm: i8} => asm{
        clc
        adc c, #imm
    }
    add c, [!{dp: u8}] => asm{
        clc
        adc c, [!dp]
    }
    add d, a => asm{
        clc
        adc d, a
    }
    add d, b => asm{
        clc
        adc d, b
    }
    add d, c => asm{
        clc
        adc d, c
    }
    add d, d => asm{
        clc
        adc d, d
    }
    add d, #{imm: i8} => asm{
        clc
        adc d, #imm
    }
    add d, [!{dp: u8}] => asm{
        clc
        adc d, [!dp]
    }
    add [!{dp: u8}], a => asm{
        clc
        adc [!dp], a
    }
    add [!{dp: u8}], b => asm{
        clc
        adc [!dp], b
    }
    add [!{dp: u8}], c => asm{
        clc
        adc [!dp], c
    }
    add [!{dp: u8}], d => asm{
        clc
        adc [!dp], d
    }
    add [!{dp: u8}], #{imm: i8} => asm{
        clc
        adc [!dp], #imm
    }

    sub a, a => asm{
        sec
        sbc a, a
    }
    sub a, b => asm{
        sec
        sbc a, b
    }
    sub a, c => asm{
        sec
        sbc a, c
    }
    sub a, d => asm{
        sec
        sbc a, d
    }
    sub a, #{imm: i8} => asm{ 
        sec
        sbc a, #imm
    }
    sub a, [!{dp: u8}] => asm{
        sec
        sbc a, [!dp]
    }
    sub b, a => asm{
        sec
        sbc b, a
    }
    sub b, b => asm{
        sec
        sbc b, b
    }
    sub b, c => asm{
        sec
        sbc b, c
    }
    sub b, d => asm{
        sec
        sbc b, d
    }
    sub b, #{imm: i8} => asm{
        sec
        sbc b, #imm
    }
    sub b, [!{dp: u8}] => asm{
        sec
        sbc b, [!dp]
    }
    sub c, a => asm{
        sec
        sbc c, a
    }
    sub c, b => asm{
        sec
        sbc c, b
    }
    sub c, c => asm{
        sec
        sbc c, c
    }
    sub c, d => asm{
        sec
        sbc c, d
    }
    sub c, #{imm: i8} => asm{
        sec
        sbc c, #imm
    }
    sub c, [!{dp: u8}] => asm{
        sec
        sbc c, [!dp]
    }
    sub d, a => asm{
        sec
        sbc d, a
    }
    sub d, b => asm{
        sec
        sbc d, b
    }
    sub d, c => asm{
        sec
        sbc d, c
    }
    sub d, d => asm{
        sec
        sbc d, d
    }
    sub d, #{imm: i8} => asm{
        sec
        sbc d, #imm
    }
    sub d, [!{dp: u8}] => asm{
        sec
        sbc d, [!dp]
    }
    sub [!{dp: u8}], a => asm{
        sec
        sbc [!dp], a
    }
    sub [!{dp: u8}], b => asm{
        sec
        sbc [!dp], b
    }
    sub [!{dp: u8}], c => asm{
        sec
        sbc [!dp], c
    }
    sub [!{dp: u8}], d => asm{
        sec
        sbc [!dp], d
    }
    sub [!{dp: u8}], #{imm: i8} => asm{
        sec
        sbc [!dp], #imm
    }

    jz {abs: u16}               => asm {je abs}
    jz {rel: bw8cpu_reladdr}    => asm {je rel}
    jz x                        => asm {je x}
    jz y                        => asm {je y}

    jnz {abs: u16}              => asm {jne abs}
    jnz {rel: bw8cpu_reladdr}   => asm {jne rel}
    jnz x                       => asm {jne x}
    jnz y                       => asm {jne y}
}