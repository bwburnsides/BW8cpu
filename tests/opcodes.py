# NOTE: This file was autogenerated by opcode_assigner.py
# Total opcode count: 508
# Zeropage opcodes: 256
# Extended opcodes: 252
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
    MOV_A_D = 0x000A
    MOV_B_A = 0x000B
    MOV_B_C = 0x000C
    MOV_B_D = 0x000D
    MOV_C_A = 0x000E
    MOV_C_B = 0x000F
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
    LOAD_A_X_C = 0x001A
    LOAD_A_X_D = 0x001B
    LOAD_A_Y_IDX = 0x001C
    LOAD_A_Y_A = 0x001D
    LOAD_A_Y_B = 0x001E
    LOAD_A_Y_C = 0x001F
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
    LOAD_B_X_A = 0x002A
    LOAD_B_X_B = 0x002B
    LOAD_B_X_C = 0x002C
    LOAD_B_X_D = 0x002D
    LOAD_B_Y_IDX = 0x002E
    LOAD_B_Y_A = 0x002F
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
    LOAD_C_DP = 0x003A
    LOAD_C_X_IDX = 0x003B
    LOAD_C_X_A = 0x003C
    LOAD_C_X_B = 0x003D
    LOAD_C_X_C = 0x003E
    LOAD_C_X_D = 0x003F
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
    LOAD_D_IMM = 0x004A
    LOAD_D_ABS = 0x004B
    LOAD_D_DP = 0x004C
    LOAD_D_X_IDX = 0x004D
    LOAD_D_X_A = 0x004E
    LOAD_D_X_B = 0x004F
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
    LOAD_D_SP_C = 0x005A
    LOAD_D_SP_D = 0x005B
    STORE_A_ABS = 0x005C
    STORE_A_DP = 0x005D
    STORE_A_X_IDX = 0x005E
    STORE_A_X_A = 0x005F
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
    STORE_A_SP_B = 0x006A
    STORE_A_SP_C = 0x006B
    STORE_A_SP_D = 0x006C
    STORE_B_ABS = 0x006D
    STORE_B_DP = 0x006E
    STORE_B_X_IDX = 0x006F
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
    STORE_B_SP_A = 0x007A
    STORE_B_SP_B = 0x007B
    STORE_B_SP_C = 0x007C
    STORE_B_SP_D = 0x007D
    STORE_C_ABS = 0x007E
    STORE_C_DP = 0x007F
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
    STORE_C_SP_IDX = 0x008A
    STORE_C_SP_A = 0x008B
    STORE_C_SP_B = 0x008C
    STORE_C_SP_C = 0x008D
    STORE_C_SP_D = 0x008E
    STORE_D_ABS = 0x008F
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
    STORE_D_Y_D = 0x009A
    STORE_D_SP_IDX = 0x009B
    STORE_D_SP_A = 0x009C
    STORE_D_SP_B = 0x009D
    STORE_D_SP_C = 0x009E
    STORE_D_SP_D = 0x009F
    MOV_X_Y = 0x00A0
    MOV_X_AB = 0x00A1
    MOV_X_CD = 0x00A2
    MOV_Y_X = 0x00A3
    MOV_Y_AB = 0x00A4
    MOV_Y_CD = 0x00A5
    MOV_AB_X = 0x00A6
    MOV_AB_Y = 0x00A7
    MOV_CD_X = 0x00A8
    MOV_CD_Y = 0x00A9
    MOV_SP_X = 0x00AA
    MOV_X_SP = 0x00AB
    LOAD_X_IMM = 0x00AC
    LOAD_X_ABS = 0x00AD
    LOAD_X_DP = 0x00AE
    LOAD_X_X_IDX = 0x00AF
    LOAD_X_Y_IDX = 0x00B0
    LOAD_X_SP_IDX = 0x00B1
    LOAD_Y_IMM = 0x00B2
    LOAD_Y_ABS = 0x00B3
    LOAD_Y_DP = 0x00B4
    LOAD_Y_X_IDX = 0x00B5
    LOAD_Y_Y_IDX = 0x00B6
    LOAD_Y_SP_IDX = 0x00B7
    STORE_X_ABS = 0x00B8
    STORE_X_DP = 0x00B9
    STORE_X_X_IDX = 0x00BA
    STORE_X_Y_IDX = 0x00BB
    STORE_X_SP_IDX = 0x00BC
    STORE_Y_ABS = 0x00BD
    STORE_Y_DP = 0x00BE
    STORE_Y_X_IDX = 0x00BF
    STORE_Y_Y_IDX = 0x00C0
    STORE_Y_SP_IDX = 0x00C1
    LEA_X_IDX = 0x00C2
    LEA_Y_IDX = 0x00C3
    LEA_SP_IDX = 0x00C4
    ADC_DP_IMM = 0x00C5
    SBC_DP_IMM = 0x00C6
    AND_DP_IMM = 0x00C7
    OR_DP_IMM = 0x00C8
    XOR_DP_IMM = 0x00C9
    NOT_DP = 0x00CA
    NEG_DP = 0x00CB
    SRC_DP = 0x00CC
    ASR_DP = 0x00CD
    INC_DP = 0x00CE
    DEC_DP = 0x00CF
    CMP_A_IMM = 0x00D0
    CMP_A_DP = 0x00D1
    CMP_B_IMM = 0x00D2
    CMP_B_DP = 0x00D3
    CMP_C_IMM = 0x00D4
    CMP_C_DP = 0x00D5
    CMP_D_IMM = 0x00D6
    CMP_D_DP = 0x00D7
    CMP_DP_A = 0x00D8
    CMP_DP_B = 0x00D9
    CMP_DP_C = 0x00DA
    CMP_DP_D = 0x00DB
    CMP_DP_IMM = 0x00DC
    TST_DP = 0x00DD
    JSR_ABS = 0x00DE
    JSR_REL = 0x00DF
    RTS = 0x00E0
    RTI = 0x00E1
    JMP_ABS = 0x00E2
    JMP_REL = 0x00E3
    JO_ABS = 0x00E4
    JO_REL = 0x00E5
    JNO_ABS = 0x00E6
    JNO_REL = 0x00E7
    JS_ABS = 0x00E8
    JS_REL = 0x00E9
    JNS_ABS = 0x00EA
    JNS_REL = 0x00EB
    JE_ABS = 0x00EC
    JE_REL = 0x00ED
    JNE_ABS = 0x00EE
    JNE_REL = 0x00EF
    JC_ABS = 0x00F0
    JC_REL = 0x00F1
    JNC_ABS = 0x00F2
    JNC_REL = 0x00F3
    JBE_ABS = 0x00F4
    JBE_REL = 0x00F5
    JA_ABS = 0x00F6
    JA_REL = 0x00F7
    JL_ABS = 0x00F8
    JL_REL = 0x00F9
    JGE_ABS = 0x00FA
    JGE_REL = 0x00FB
    JLE_ABS = 0x00FC
    JLE_REL = 0x00FD
    JG_ABS = 0x00FE
    JG_REL = 0x00FF

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
    OUT_A = 0x010A
    OUT_B = 0x010B
    OUT_C = 0x010C
    OUT_D = 0x010D
    OUT_DP = 0x010E
    OUT_IMM = 0x010F
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
    LEA_SP_C = 0x011A
    LEA_SP_D = 0x011B
    ADC_A_A = 0x011C
    ADC_A_B = 0x011D
    ADC_A_C = 0x011E
    ADC_A_D = 0x011F
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
    ADC_C_C = 0x012A
    ADC_C_D = 0x012B
    ADC_C_IMM = 0x012C
    ADC_C_DP = 0x012D
    ADC_D_A = 0x012E
    ADC_D_B = 0x012F
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
    SBC_A_C = 0x013A
    SBC_A_D = 0x013B
    SBC_A_IMM = 0x013C
    SBC_A_DP = 0x013D
    SBC_B_A = 0x013E
    SBC_B_B = 0x013F
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
    SBC_D_A = 0x014A
    SBC_D_B = 0x014B
    SBC_D_C = 0x014C
    SBC_D_D = 0x014D
    SBC_D_IMM = 0x014E
    SBC_D_DP = 0x014F
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
    AND_B_C = 0x015A
    AND_B_D = 0x015B
    AND_B_IMM = 0x015C
    AND_B_DP = 0x015D
    AND_C_A = 0x015E
    AND_C_B = 0x015F
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
    AND_DP_C = 0x016A
    AND_DP_D = 0x016B
    OR_A_B = 0x016C
    OR_A_C = 0x016D
    OR_A_D = 0x016E
    OR_A_IMM = 0x016F
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
    OR_C_DP = 0x017A
    OR_D_A = 0x017B
    OR_D_B = 0x017C
    OR_D_C = 0x017D
    OR_D_IMM = 0x017E
    OR_D_DP = 0x017F
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
    XOR_B_A = 0x018A
    XOR_B_B = 0x018B
    XOR_B_C = 0x018C
    XOR_B_D = 0x018D
    XOR_B_IMM = 0x018E
    XOR_B_DP = 0x018F
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
    XOR_D_IMM = 0x019A
    XOR_D_DP = 0x019B
    XOR_DP_A = 0x019C
    XOR_DP_B = 0x019D
    XOR_DP_C = 0x019E
    XOR_DP_D = 0x019F
    NOT_A = 0x01A0
    NOT_B = 0x01A1
    NOT_C = 0x01A2
    NOT_D = 0x01A3
    NEG_A = 0x01A4
    NEG_B = 0x01A5
    NEG_C = 0x01A6
    NEG_D = 0x01A7
    SRC_A = 0x01A8
    SRC_B = 0x01A9
    SRC_C = 0x01AA
    SRC_D = 0x01AB
    ASR_A = 0x01AC
    ASR_B = 0x01AD
    ASR_C = 0x01AE
    ASR_D = 0x01AF
    INC_A = 0x01B0
    INC_B = 0x01B1
    INC_C = 0x01B2
    INC_D = 0x01B3
    INC_X = 0x01B4
    INC_Y = 0x01B5
    DEC_A = 0x01B6
    DEC_B = 0x01B7
    DEC_C = 0x01B8
    DEC_D = 0x01B9
    DEC_X = 0x01BA
    DEC_Y = 0x01BB
    PUSH_A = 0x01BC
    PUSH_B = 0x01BD
    PUSH_C = 0x01BE
    PUSH_D = 0x01BF
    PUSH_X = 0x01C0
    PUSH_Y = 0x01C1
    POP_A = 0x01C2
    POP_B = 0x01C3
    POP_C = 0x01C4
    POP_D = 0x01C5
    POP_X = 0x01C6
    POP_Y = 0x01C7
    CMP_A_A = 0x01C8
    CMP_A_B = 0x01C9
    CMP_A_C = 0x01CA
    CMP_A_D = 0x01CB
    CMP_B_A = 0x01CC
    CMP_B_B = 0x01CD
    CMP_B_C = 0x01CE
    CMP_B_D = 0x01CF
    CMP_C_A = 0x01D0
    CMP_C_B = 0x01D1
    CMP_C_C = 0x01D2
    CMP_C_D = 0x01D3
    CMP_D_A = 0x01D4
    CMP_D_B = 0x01D5
    CMP_D_C = 0x01D6
    CMP_D_D = 0x01D7
    TST_A = 0x01D8
    TST_B = 0x01D9
    TST_C = 0x01DA
    TST_D = 0x01DB
    JSR_X = 0x01DC
    JSR_Y = 0x01DD
    JMP_X = 0x01DE
    JMP_Y = 0x01DF
    JO_X = 0x01E0
    JO_Y = 0x01E1
    JNO_X = 0x01E2
    JNO_Y = 0x01E3
    JS_X = 0x01E4
    JS_Y = 0x01E5
    JNS_X = 0x01E6
    JNS_Y = 0x01E7
    JE_X = 0x01E8
    JE_Y = 0x01E9
    JNE_X = 0x01EA
    JNE_Y = 0x01EB
    JC_X = 0x01EC
    JC_Y = 0x01ED
    JNC_X = 0x01EE
    JNC_Y = 0x01EF
    JBE_X = 0x01F0
    JBE_Y = 0x01F1
    JA_X = 0x01F2
    JA_Y = 0x01F3
    JL_X = 0x01F4
    JL_Y = 0x01F5
    JGE_X = 0x01F6
    JGE_Y = 0x01F7
    JLE_X = 0x01F8
    JLE_Y = 0x01F9
    JG_X = 0x01FA
    JG_Y = 0x01FB
