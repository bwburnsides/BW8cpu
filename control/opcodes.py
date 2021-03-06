# NOTE: This file was autogenerated by build_opcodes.py
# Total opcode count: 509
# Zeropage opcodes: 256
# Extended opcodes: 253
import enum
class Op(enum.IntEnum):
    NOP = 0x0000
    EXT = 0x0001
    CLC = 0x0002
    CLI = 0x0003
    CLV = 0x0004
    SEC = 0x0005
    SEI = 0x0006
    UBR = 0x0007
    MOV_A_B = 0x0008
    MOV_A_C = 0x0009
    MOV_A_D = 0x000a
    MOV_B_A = 0x000b
    MOV_B_C = 0x000c
    MOV_B_D = 0x000d
    MOV_C_A = 0x000e
    MOV_C_B = 0x000f
    MOV_C_D = 0x0010
    MOV_D_A = 0x0011
    MOV_D_B = 0x0012
    MOV_D_C = 0x0013
    LOAD_A_IMM = 0x0014
    LOAD_A_ABS = 0x0015
    LOAD_A_DP = 0x0016
    LOAD_A_X_IDX = 0x0017
    LOAD_A_X_A = 0x0018
    LOAD_A_X_B = 0x0019
    LOAD_A_X_C = 0x001a
    LOAD_A_X_D = 0x001b
    LOAD_A_Y_IDX = 0x001c
    LOAD_A_Y_A = 0x001d
    LOAD_A_Y_B = 0x001e
    LOAD_A_Y_C = 0x001f
    LOAD_A_Y_D = 0x0020
    LOAD_A_SP_IDX = 0x0021
    LOAD_A_SP_A = 0x0022
    LOAD_A_SP_B = 0x0023
    LOAD_A_SP_C = 0x0024
    LOAD_A_SP_D = 0x0025
    LOAD_B_IMM = 0x0026
    LOAD_B_ABS = 0x0027
    LOAD_B_DP = 0x0028
    LOAD_B_X_IDX = 0x0029
    LOAD_B_X_A = 0x002a
    LOAD_B_X_B = 0x002b
    LOAD_B_X_C = 0x002c
    LOAD_B_X_D = 0x002d
    LOAD_B_Y_IDX = 0x002e
    LOAD_B_Y_A = 0x002f
    LOAD_B_Y_B = 0x0030
    LOAD_B_Y_C = 0x0031
    LOAD_B_Y_D = 0x0032
    LOAD_B_SP_IDX = 0x0033
    LOAD_B_SP_A = 0x0034
    LOAD_B_SP_B = 0x0035
    LOAD_B_SP_C = 0x0036
    LOAD_B_SP_D = 0x0037
    LOAD_C_IMM = 0x0038
    LOAD_C_ABS = 0x0039
    LOAD_C_DP = 0x003a
    LOAD_C_X_IDX = 0x003b
    LOAD_C_X_A = 0x003c
    LOAD_C_X_B = 0x003d
    LOAD_C_X_C = 0x003e
    LOAD_C_X_D = 0x003f
    LOAD_C_Y_IDX = 0x0040
    LOAD_C_Y_A = 0x0041
    LOAD_C_Y_B = 0x0042
    LOAD_C_Y_C = 0x0043
    LOAD_C_Y_D = 0x0044
    LOAD_C_SP_IDX = 0x0045
    LOAD_C_SP_A = 0x0046
    LOAD_C_SP_B = 0x0047
    LOAD_C_SP_C = 0x0048
    LOAD_C_SP_D = 0x0049
    LOAD_D_IMM = 0x004a
    LOAD_D_ABS = 0x004b
    LOAD_D_DP = 0x004c
    LOAD_D_X_IDX = 0x004d
    LOAD_D_X_A = 0x004e
    LOAD_D_X_B = 0x004f
    LOAD_D_X_C = 0x0050
    LOAD_D_X_D = 0x0051
    LOAD_D_Y_IDX = 0x0052
    LOAD_D_Y_A = 0x0053
    LOAD_D_Y_B = 0x0054
    LOAD_D_Y_C = 0x0055
    LOAD_D_Y_D = 0x0056
    LOAD_D_SP_IDX = 0x0057
    LOAD_D_SP_A = 0x0058
    LOAD_D_SP_B = 0x0059
    LOAD_D_SP_C = 0x005a
    LOAD_D_SP_D = 0x005b
    STORE_A_ABS = 0x005c
    STORE_A_DP = 0x005d
    STORE_A_X_IDX = 0x005e
    STORE_A_X_A = 0x005f
    STORE_A_X_B = 0x0060
    STORE_A_X_C = 0x0061
    STORE_A_X_D = 0x0062
    STORE_A_Y_IDX = 0x0063
    STORE_A_Y_A = 0x0064
    STORE_A_Y_B = 0x0065
    STORE_A_Y_C = 0x0066
    STORE_A_Y_D = 0x0067
    STORE_A_SP_IDX = 0x0068
    STORE_A_SP_A = 0x0069
    STORE_A_SP_B = 0x006a
    STORE_A_SP_C = 0x006b
    STORE_A_SP_D = 0x006c
    STORE_B_ABS = 0x006d
    STORE_B_DP = 0x006e
    STORE_B_X_IDX = 0x006f
    STORE_B_X_A = 0x0070
    STORE_B_X_B = 0x0071
    STORE_B_X_C = 0x0072
    STORE_B_X_D = 0x0073
    STORE_B_Y_IDX = 0x0074
    STORE_B_Y_A = 0x0075
    STORE_B_Y_B = 0x0076
    STORE_B_Y_C = 0x0077
    STORE_B_Y_D = 0x0078
    STORE_B_SP_IDX = 0x0079
    STORE_B_SP_A = 0x007a
    STORE_B_SP_B = 0x007b
    STORE_B_SP_C = 0x007c
    STORE_B_SP_D = 0x007d
    STORE_C_ABS = 0x007e
    STORE_C_DP = 0x007f
    STORE_C_X_IDX = 0x0080
    STORE_C_X_A = 0x0081
    STORE_C_X_B = 0x0082
    STORE_C_X_C = 0x0083
    STORE_C_X_D = 0x0084
    STORE_C_Y_IDX = 0x0085
    STORE_C_Y_A = 0x0086
    STORE_C_Y_B = 0x0087
    STORE_C_Y_C = 0x0088
    STORE_C_Y_D = 0x0089
    STORE_C_SP_IDX = 0x008a
    STORE_C_SP_A = 0x008b
    STORE_C_SP_B = 0x008c
    STORE_C_SP_C = 0x008d
    STORE_C_SP_D = 0x008e
    STORE_D_ABS = 0x008f
    STORE_D_DP = 0x0090
    STORE_D_X_IDX = 0x0091
    STORE_D_X_A = 0x0092
    STORE_D_X_B = 0x0093
    STORE_D_X_C = 0x0094
    STORE_D_X_D = 0x0095
    STORE_D_Y_IDX = 0x0096
    STORE_D_Y_A = 0x0097
    STORE_D_Y_B = 0x0098
    STORE_D_Y_C = 0x0099
    STORE_D_Y_D = 0x009a
    STORE_D_SP_IDX = 0x009b
    STORE_D_SP_A = 0x009c
    STORE_D_SP_B = 0x009d
    STORE_D_SP_C = 0x009e
    STORE_D_SP_D = 0x009f
    MOV_X_Y = 0x00a0
    MOV_X_AB = 0x00a1
    MOV_X_CD = 0x00a2
    MOV_Y_X = 0x00a3
    MOV_Y_AB = 0x00a4
    MOV_Y_CD = 0x00a5
    MOV_AB_X = 0x00a6
    MOV_AB_Y = 0x00a7
    MOV_CD_X = 0x00a8
    MOV_CD_Y = 0x00a9
    MOV_SP_X = 0x00aa
    MOV_X_SP = 0x00ab
    LOAD_X_IMM = 0x00ac
    LOAD_X_ABS = 0x00ad
    LOAD_X_DP = 0x00ae
    LOAD_X_X_IDX = 0x00af
    LOAD_X_Y_IDX = 0x00b0
    LOAD_X_SP_IDX = 0x00b1
    LOAD_Y_IMM = 0x00b2
    LOAD_Y_ABS = 0x00b3
    LOAD_Y_DP = 0x00b4
    LOAD_Y_X_IDX = 0x00b5
    LOAD_Y_Y_IDX = 0x00b6
    LOAD_Y_SP_IDX = 0x00b7
    STORE_X_ABS = 0x00b8
    STORE_X_DP = 0x00b9
    STORE_X_X_IDX = 0x00ba
    STORE_X_Y_IDX = 0x00bb
    STORE_X_SP_IDX = 0x00bc
    STORE_Y_ABS = 0x00bd
    STORE_Y_DP = 0x00be
    STORE_Y_X_IDX = 0x00bf
    STORE_Y_Y_IDX = 0x00c0
    STORE_Y_SP_IDX = 0x00c1
    LEA_X_IDX = 0x00c2
    LEA_Y_IDX = 0x00c3
    LEA_SP_IDX = 0x00c4
    ADC_DP_IMM = 0x00c5
    SBC_DP_IMM = 0x00c6
    AND_DP_IMM = 0x00c7
    OR_DP_IMM = 0x00c8
    XOR_DP_IMM = 0x00c9
    NOT_DP = 0x00ca
    NEG_DP = 0x00cb
    SRC_DP = 0x00cc
    ASR_DP = 0x00cd
    INC_DP = 0x00ce
    DEC_DP = 0x00cf
    CMP_A_IMM = 0x00d0
    CMP_A_DP = 0x00d1
    CMP_B_IMM = 0x00d2
    CMP_B_DP = 0x00d3
    CMP_C_IMM = 0x00d4
    CMP_C_DP = 0x00d5
    CMP_D_IMM = 0x00d6
    CMP_D_DP = 0x00d7
    CMP_DP_A = 0x00d8
    CMP_DP_B = 0x00d9
    CMP_DP_C = 0x00da
    CMP_DP_D = 0x00db
    CMP_DP_IMM = 0x00dc
    TST_DP = 0x00dd
    JSR_ABS = 0x00de
    JSR_REL = 0x00df
    RTS = 0x00e0
    RTI = 0x00e1
    JMP_ABS = 0x00e2
    JMP_REL = 0x00e3
    JO_ABS = 0x00e4
    JO_REL = 0x00e5
    JNO_ABS = 0x00e6
    JNO_REL = 0x00e7
    JS_ABS = 0x00e8
    JS_REL = 0x00e9
    JNS_ABS = 0x00ea
    JNS_REL = 0x00eb
    JE_ABS = 0x00ec
    JE_REL = 0x00ed
    JNE_ABS = 0x00ee
    JNE_REL = 0x00ef
    JC_ABS = 0x00f0
    JC_REL = 0x00f1
    JNC_ABS = 0x00f2
    JNC_REL = 0x00f3
    JBE_ABS = 0x00f4
    JBE_REL = 0x00f5
    JA_ABS = 0x00f6
    JA_REL = 0x00f7
    JL_ABS = 0x00f8
    JL_REL = 0x00f9
    JGE_ABS = 0x00fa
    JGE_REL = 0x00fb
    JLE_ABS = 0x00fc
    JLE_REL = 0x00fd
    JG_ABS = 0x00fe
    JG_REL = 0x00ff

    KBR = 0x0100
    MOV_A_DP = 0x0101
    MOV_DP_A = 0x0102
    MOV_BR_A = 0x0103
    MOV_A_BR = 0x0104
    IN_A = 0x0105
    IN_B = 0x0106
    IN_C = 0x0107
    IN_D = 0x0108
    IN_DP = 0x0109
    OUT_A = 0x010a
    OUT_B = 0x010b
    OUT_C = 0x010c
    OUT_D = 0x010d
    OUT_DP = 0x010e
    OUT_IMM = 0x010f
    LEA_X_A = 0x0110
    LEA_X_B = 0x0111
    LEA_X_C = 0x0112
    LEA_X_D = 0x0113
    LEA_Y_A = 0x0114
    LEA_Y_B = 0x0115
    LEA_Y_C = 0x0116
    LEA_Y_D = 0x0117
    LEA_SP_A = 0x0118
    LEA_SP_B = 0x0119
    LEA_SP_C = 0x011a
    LEA_SP_D = 0x011b
    ADC_A_A = 0x011c
    ADC_A_B = 0x011d
    ADC_A_C = 0x011e
    ADC_A_D = 0x011f
    ADC_A_IMM = 0x0120
    ADC_A_DP = 0x0121
    ADC_B_A = 0x0122
    ADC_B_B = 0x0123
    ADC_B_C = 0x0124
    ADC_B_D = 0x0125
    ADC_B_IMM = 0x0126
    ADC_B_DP = 0x0127
    ADC_C_A = 0x0128
    ADC_C_B = 0x0129
    ADC_C_C = 0x012a
    ADC_C_D = 0x012b
    ADC_C_IMM = 0x012c
    ADC_C_DP = 0x012d
    ADC_D_A = 0x012e
    ADC_D_B = 0x012f
    ADC_D_C = 0x0130
    ADC_D_D = 0x0131
    ADC_D_IMM = 0x0132
    ADC_D_DP = 0x0133
    ADC_DP_A = 0x0134
    ADC_DP_B = 0x0135
    ADC_DP_C = 0x0136
    ADC_DP_D = 0x0137
    SBC_A_A = 0x0138
    SBC_A_B = 0x0139
    SBC_A_C = 0x013a
    SBC_A_D = 0x013b
    SBC_A_IMM = 0x013c
    SBC_A_DP = 0x013d
    SBC_B_A = 0x013e
    SBC_B_B = 0x013f
    SBC_B_C = 0x0140
    SBC_B_D = 0x0141
    SBC_B_IMM = 0x0142
    SBC_B_DP = 0x0143
    SBC_C_A = 0x0144
    SBC_C_B = 0x0145
    SBC_C_C = 0x0146
    SBC_C_D = 0x0147
    SBC_C_IMM = 0x0148
    SBC_C_DP = 0x0149
    SBC_D_A = 0x014a
    SBC_D_B = 0x014b
    SBC_D_C = 0x014c
    SBC_D_D = 0x014d
    SBC_D_IMM = 0x014e
    SBC_D_DP = 0x014f
    SBC_DP_A = 0x0150
    SBC_DP_B = 0x0151
    SBC_DP_C = 0x0152
    SBC_DP_D = 0x0153
    AND_A_B = 0x0154
    AND_A_C = 0x0155
    AND_A_D = 0x0156
    AND_A_IMM = 0x0157
    AND_A_DP = 0x0158
    AND_B_A = 0x0159
    AND_B_C = 0x015a
    AND_B_D = 0x015b
    AND_B_IMM = 0x015c
    AND_B_DP = 0x015d
    AND_C_A = 0x015e
    AND_C_B = 0x015f
    AND_C_D = 0x0160
    AND_C_IMM = 0x0161
    AND_C_DP = 0x0162
    AND_D_A = 0x0163
    AND_D_B = 0x0164
    AND_D_C = 0x0165
    AND_D_IMM = 0x0166
    AND_D_DP = 0x0167
    AND_DP_A = 0x0168
    AND_DP_B = 0x0169
    AND_DP_C = 0x016a
    AND_DP_D = 0x016b
    OR_A_B = 0x016c
    OR_A_C = 0x016d
    OR_A_D = 0x016e
    OR_A_IMM = 0x016f
    OR_A_DP = 0x0170
    OR_B_A = 0x0171
    OR_B_C = 0x0172
    OR_B_D = 0x0173
    OR_B_IMM = 0x0174
    OR_B_DP = 0x0175
    OR_C_A = 0x0176
    OR_C_B = 0x0177
    OR_C_D = 0x0178
    OR_C_IMM = 0x0179
    OR_C_DP = 0x017a
    OR_D_A = 0x017b
    OR_D_B = 0x017c
    OR_D_C = 0x017d
    OR_D_IMM = 0x017e
    OR_D_DP = 0x017f
    OR_DP_A = 0x0180
    OR_DP_B = 0x0181
    OR_DP_C = 0x0182
    OR_DP_D = 0x0183
    XOR_A_A = 0x0184
    XOR_A_B = 0x0185
    XOR_A_C = 0x0186
    XOR_A_D = 0x0187
    XOR_A_IMM = 0x0188
    XOR_A_DP = 0x0189
    XOR_B_A = 0x018a
    XOR_B_B = 0x018b
    XOR_B_C = 0x018c
    XOR_B_D = 0x018d
    XOR_B_IMM = 0x018e
    XOR_B_DP = 0x018f
    XOR_C_A = 0x0190
    XOR_C_B = 0x0191
    XOR_C_C = 0x0192
    XOR_C_D = 0x0193
    XOR_C_IMM = 0x0194
    XOR_C_DP = 0x0195
    XOR_D_A = 0x0196
    XOR_D_B = 0x0197
    XOR_D_C = 0x0198
    XOR_D_D = 0x0199
    XOR_D_IMM = 0x019a
    XOR_D_DP = 0x019b
    XOR_DP_A = 0x019c
    XOR_DP_B = 0x019d
    XOR_DP_C = 0x019e
    XOR_DP_D = 0x019f
    NOT_A = 0x01a0
    NOT_B = 0x01a1
    NOT_C = 0x01a2
    NOT_D = 0x01a3
    NEG_A = 0x01a4
    NEG_B = 0x01a5
    NEG_C = 0x01a6
    NEG_D = 0x01a7
    SRC_A = 0x01a8
    SRC_B = 0x01a9
    SRC_C = 0x01aa
    SRC_D = 0x01ab
    ASR_A = 0x01ac
    ASR_B = 0x01ad
    ASR_C = 0x01ae
    ASR_D = 0x01af
    INC_A = 0x01b0
    INC_B = 0x01b1
    INC_C = 0x01b2
    INC_D = 0x01b3
    INC_X = 0x01b4
    INC_Y = 0x01b5
    DEC_A = 0x01b6
    DEC_B = 0x01b7
    DEC_C = 0x01b8
    DEC_D = 0x01b9
    DEC_X = 0x01ba
    DEC_Y = 0x01bb
    PUSH_A = 0x01bc
    PUSH_B = 0x01bd
    PUSH_C = 0x01be
    PUSH_D = 0x01bf
    PUSH_X = 0x01c0
    PUSH_Y = 0x01c1
    POP_A = 0x01c2
    POP_B = 0x01c3
    POP_C = 0x01c4
    POP_D = 0x01c5
    POP_X = 0x01c6
    POP_Y = 0x01c7
    CMP_A_A = 0x01c8
    CMP_A_B = 0x01c9
    CMP_A_C = 0x01ca
    CMP_A_D = 0x01cb
    CMP_B_A = 0x01cc
    CMP_B_B = 0x01cd
    CMP_B_C = 0x01ce
    CMP_B_D = 0x01cf
    CMP_C_A = 0x01d0
    CMP_C_B = 0x01d1
    CMP_C_C = 0x01d2
    CMP_C_D = 0x01d3
    CMP_D_A = 0x01d4
    CMP_D_B = 0x01d5
    CMP_D_C = 0x01d6
    CMP_D_D = 0x01d7
    TST_A = 0x01d8
    TST_B = 0x01d9
    TST_C = 0x01da
    TST_D = 0x01db
    JSR_X = 0x01dc
    JSR_Y = 0x01dd
    JMP_X = 0x01de
    JMP_Y = 0x01df
    JO_X = 0x01e0
    JO_Y = 0x01e1
    JNO_X = 0x01e2
    JNO_Y = 0x01e3
    JS_X = 0x01e4
    JS_Y = 0x01e5
    JNS_X = 0x01e6
    JNS_Y = 0x01e7
    JE_X = 0x01e8
    JE_Y = 0x01e9
    JNE_X = 0x01ea
    JNE_Y = 0x01eb
    JC_X = 0x01ec
    JC_Y = 0x01ed
    JNC_X = 0x01ee
    JNC_Y = 0x01ef
    JBE_X = 0x01f0
    JBE_Y = 0x01f1
    JA_X = 0x01f2
    JA_Y = 0x01f3
    JL_X = 0x01f4
    JL_Y = 0x01f5
    JGE_X = 0x01f6
    JGE_Y = 0x01f7
    JLE_X = 0x01f8
    JLE_Y = 0x01f9
    JG_X = 0x01fa
    JG_Y = 0x01fb
    HALT = 0x01fc

