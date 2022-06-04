from enum import IntEnum
from logging import PlaceHolder
from tkinter import Place


class GenPurpReg(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3


# 3 bits
class IntReg(IntEnum):
    DP = 0
    DA = 1
    TH = 2
    TL = 3
    IR = 4
    SR = 5
    OF = 6
    BR = 7


# 2 bits
class AddrReg(IntEnum):
    PC = 0
    SP = 1
    X = 2
    Y = 3


# 2 bits
class CPUMode(IntEnum):
    FETCH = 0
    IRQ = 1
    NMI = 2
    STALL = 3


class AddrAssert(IntEnum):
    ACK = 0
    PC = 1
    SP = 2
    X = 3
    Y = 4
    DP = 5
    T = 6
    IO = 7


class DbusAssert(IntEnum):
    ALU = 0
    A = 1
    B = 2
    C = 3
    D = 4
    DP = 5
    DA = 6
    TH = 7
    TL = 8
    SR = 9
    MEM = 10
    MSB = 11
    LSB = 12
    BR = 13
    PlaceHolder14 = 14
    PlaceHolder15 = 15


class XferAssert(IntEnum):
    PC = 0
    SP = 1
    X = 2
    Y = 3
    IRQ = 4
    ADDR = 5
    A_A = 6
    A_B = 7
    A_C = 8
    A_D = 9
    A_TL = 10
    B_A = 11
    B_B = 12
    B_C = 13
    B_D = 14
    B_TL = 15
    C_A = 16
    C_B = 17
    C_C = 18
    C_D = 19
    C_TL = 20
    D_A = 21
    D_B = 22
    D_C = 23
    D_D = 24
    D_TL = 25
    TH_A = 26
    TH_B = 27
    TH_C = 28
    TH_D = 29
    T = 30
    NMI = 31


class DbusLoad(IntEnum):
    NULL = 0
    A = 1
    B = 2
    C = 3
    D = 4
    DP = 5
    DA = 6
    TH = 7
    TL = 8
    SR = 9
    MEM = 10
    IR = 11
    OFF = 12
    PCH = 13
    PCL = 14
    SPH = 15
    SPL = 16
    XH = 17
    XL = 18
    YH = 19
    YL = 20
    BR = 21
    SET_USE_BR = 22
    CLR_USE_BR = 23
    SET_SUPER_MODE = 24
    CLR_SUPER_MODE = 25
    SET_NMI_MASK = 26
    CLR_NMI_MASK = 27
    PlaceHolder28 = 28
    PlaceHolder29 = 29
    PlaceHolder30 = 30
    PlaceHolder31 = 31


class XferLoad(IntEnum):
    NULL = 0
    PC = 1
    SP = 2
    X = 3
    Y = 4
    AB = 5
    CD = 6
    PlaceHolder7 = 7


class Count(IntEnum):
    NULL = 0
    INC_PC = 1
    INC_SP = 2
    INC_X = 3
    INC_Y = 4
    INC_ADDR = 5
    DEC_X = 6
    DEC_Y = 7


class ALUShiftFunc(IntEnum):
    LHS = 0
    SRC = 1
    ASR = 2
    ZERO = 3

    DONT_CARE = ZERO


class ALULogicFunc(IntEnum):
    ZERO = 0b0000
    MAX = 0b1111
    A = LHS = 0b1010
    B = RHS = 0b1100
    notA = notLHS = 0b0101
    notB = notRHS = 0b0011
    OR = 0b1110
    AND = 0b1000
    XOR = 0b0110

    DONT_CARE = MAX


class ALUSumFunc(IntEnum):
    ZERO = 0b00
    Cf = 0b01
    ONE = 0b11

    DONT_CARE = ONE


class CfFunc(IntEnum):
    SET = 0b000
    C_SHIFT = 0b001
    C_SUM = 0b010
    CLEAR = 0b011
    NO_CHANGE = 0b111


class ZVNfFunc(IntEnum):
    SET = 0b00
    NEW = 0b01
    CLEAR = 0b10
    NO_CHANGE = 0b11


ZfFunc = ZVNfFunc
VfFunc = ZVNfFunc
NfFunc = ZVNfFunc


class IfFunc(IntEnum):
    SET = 0b00
    CLEAR = 0b01
    NO_CHANGE = 0b11
