from dataclasses import dataclass
from enum import Enum


class Ctrl:
    # Ctrl Latch 0: DBUS_ASSERT, ALU_OP
    # Ctrl Latch 1: DBUS_LOAD, ADDR_ASSERT
    # Ctrl Latch 2: XFER_ASSERT, XFER_LOAD
    # Ctrl Latch 3: COUNT, RST_USEQ, SET_EXT, OFFSET, BRK_CLK

    # 4 bits for DBUS Assert
    DBUS_ASSERT_ALU = 0 << 0
    DBUS_ASSERT_A = 1 << 0
    DBUS_ASSERT_B = 2 << 0
    DBUS_ASSERT_C = 3 << 0
    DBUS_ASSERT_D = 4 << 0
    DBUS_ASSERT_DP = 5 << 0
    DBUS_ASSERT_DA = 6 << 0
    DBUS_ASSERT_TH = 7 << 0
    DBUS_ASSERT_TL = 8 << 0
    DBUS_ASSERT_SR = 9 << 0
    DBUS_ASSERT_MEM = 10 << 0
    DBUS_ASSERT_MSB = 11 << 0
    DBUS_ASSERT_LSB = 12 << 0
    DBUS_ASSERT_BR = 13 << 0

    # 4 bits for ALU OP
    ALU_NOP = 0 << 4
    ALU_ADC = 1 << 4
    ALU_SBC = 2 << 4
    ALU_INC = 3 << 4
    ALU_DEC = 4 << 4
    ALU_AND = 5 << 4
    ALU_OR = 6 << 4
    ALU_XOR = 7 << 4
    ALU_NOT = 8 << 4
    ALU_SRC = 9 << 4
    ALU_ASR = 10 << 4
    ALU_SEI = 11 << 4
    ALU_CLI = 12 << 4
    ALU_SEC = 13 << 4
    ALU_CLC = 14 << 4
    ALU_CLV = 15 << 4

    # 5 bits for DBUS Load
    DBUS_LOAD_NULL = 0 << 8
    DBUS_LOAD_A = 1 << 8
    DBUS_LOAD_B = 2 << 8
    DBUS_LOAD_C = 3 << 8
    DBUS_LOAD_D = 4 << 8
    DBUS_LOAD_DP = 5 << 8
    DBUS_LOAD_DA = 6 << 8
    DBUS_LOAD_TH = 7 << 8
    DBUS_LOAD_TL = 8 << 8
    DBUS_LOAD_SR = 9 << 8
    DBUS_LOAD_MEM = 10 << 8
    DBUS_LOAD_IR = 11 << 8
    DBUS_LOAD_OFF = 12 << 8
    DBUS_LOAD_PCH = 13 << 8
    DBUS_LOAD_PCL = 14 << 8
    DBUS_LOAD_SPH = 15 << 8
    DBUS_LOAD_SPL = 16 << 8
    DBUS_LOAD_XH = 17 << 8
    DBUS_LOAD_XL = 18 << 8
    DBUS_LOAD_YH = 19 << 8
    DBUS_LOAD_YL = 20 << 8
    DBUS_LOAD_BR = 21 << 8
    SET_USE_BR = 22 << 8
    CLR_USE_BR = 23 << 8
    SET_SUPER_MODE = 24 << 8
    CLR_SUPER_MODE = 25 << 8
    SET_NMI_MASK = 26 << 8
    CLR_NMI_MASK = 27 << 8
    DBUS_LOAD_PORT = DBUS_LOAD_TL

    # 3 bits for ADDR Assert
    ADDR_ASSERT_ACK = 0 << 13
    ADDR_ASSERT_PC = 1 << 13
    ADDR_ASSERT_SP = 2 << 13
    ADDR_ASSERT_X = 3 << 13
    ADDR_ASSERT_Y = 4 << 13
    ADDR_ASSERT_DP = 5 << 13
    ADDR_ASSERT_T = 6 << 13
    ADDR_ASSERT_IO = 7 << 13

    # 5 bits for XFER Assert
    XFER_ASSERT_PC = 0 << 16
    XFER_ASSERT_SP = 1 << 16
    XFER_ASSERT_X = 2 << 16
    XFER_ASSERT_Y = 3 << 16
    XFER_ASSERT_IRQ = 4 << 16
    XFER_ASSERT_ADDR = 5 << 16
    XFER_ASSERT_A_A = 6 << 16
    XFER_ASSERT_A_B = 7 << 16
    XFER_ASSERT_A_C = 8 << 16
    XFER_ASSERT_A_D = 9 << 16
    XFER_ASSERT_A_TL = 10 << 16
    XFER_ASSERT_B_A = 11 << 16
    XFER_ASSERT_B_B = 12 << 16
    XFER_ASSERT_B_C = 13 << 16
    XFER_ASSERT_B_D = 14 << 16
    XFER_ASSERT_B_TL = 15 << 16
    XFER_ASSERT_C_A = 16 << 16
    XFER_ASSERT_C_B = 17 << 16
    XFER_ASSERT_C_C = 18 << 16
    XFER_ASSERT_C_D = 19 << 16
    XFER_ASSERT_C_TL = 20 << 16
    XFER_ASSERT_D_A = 21 << 16
    XFER_ASSERT_D_B = 22 << 16
    XFER_ASSERT_D_C = 23 << 16
    XFER_ASSERT_D_D = 24 << 16
    XFER_ASSERT_D_TL = 25 << 16
    XFER_ASSERT_TH_A = 26 << 16
    XFER_ASSERT_TH_B = 27 << 16
    XFER_ASSERT_TH_C = 28 << 16
    XFER_ASSERT_TH_D = 29 << 16
    XFER_ASSERT_T = 30 << 16
    XFER_ASSERT_NMI = 31 << 16

    # 3 bits for XFER Load
    XFER_LOAD_NULL = 0 << 21
    XFER_LOAD_PC = 1 << 21
    XFER_LOAD_SP = 2 << 21
    XFER_LOAD_X = 3 << 21
    XFER_LOAD_Y = 4 << 21
    XFER_LOAD_AB = 5 << 21
    XFER_LOAD_CD = 6 << 21

    # 3 bits for Counter Inc/Decs
    COUNT_NULL = 0 << 24
    COUNT_INC_PC = 1 << 24
    COUNT_INC_SP = 2 << 24
    COUNT_INC_X = 3 << 24
    COUNT_INC_Y = 4 << 24
    COUNT_INC_ADDR = 5 << 24
    COUNT_DEC_X = 6 << 24
    COUNT_DEC_Y = 7 << 24

    # 1 bit for SP Dec
    # (Allows SP to be prepped for push while operand is being fetched)
    COUNT_DEC_SP = 1 << 27

    # 4 bit fields for CPU CTRL
    RST_USEQ = 1 << 28
    TOG_EXT = 1 << 29
    OFFSET = 1 << 30
    BRK_CLK = 1 << 31

    @staticmethod
    def decode(word: int) -> str:
        DBUS_ASSERT = (word >> 0) & (2**4 - 1)
        DBUS_LOAD = (word >> 4) & (2**5 - 1)
        ALU_OP = (word >> 9) & (2**4 - 1)
        XFER_ASSERT = (word >> 13) & (2**5 - 1)
        XFER_LOAD = (word >> 18) & (2**3 - 1)
        ADDR_ASSERT = (word >> 21) & (2**3 - 1)
        COUNT = (word >> 24) & (2**3 - 1)
        DEC_SP = (word >> 27) & (2**1 - 1)
        RST_USEQ = (word >> 28) & (2**1 - 1)
        TOG_EXT = (word >> 29) & (2**1 - 1)
        OFFSET = (word >> 30) & (2**1 - 1)
        BRK_CLK = (word >> 31) & (2**1 - 1)

        return "\n".join(
            [
                f"DBUS_ASSERT: {DBUS_ASSERT}",
                f"DBUS_LOAD: {DBUS_LOAD}",
                f"ALU_OP: {ALU_OP}",
                f"XFER_ASSERT: {XFER_ASSERT}",
                f"XFER_LOAD: {XFER_LOAD}",
                f"ADDR_ASSERT: {ADDR_ASSERT}",
                f"COUNT: {COUNT}",
                f"DEC_SP: {DEC_SP}",
                f"RST_USEQ: {RST_USEQ}",
                f"TOG_EXT: {TOG_EXT}",
                f"OFFSET: {OFFSET}",
                f"BRK_CLK: {BRK_CLK}\n",
            ]
        )


@dataclass
class Flags:
    N: bool
    V: bool
    Z: bool
    C: bool

    def __init__(self, packed_flags: int):
        self.N = bool((packed_flags >> 3) & 8)
        self.V = bool((packed_flags >> 2) & 4)
        self.Z = bool((packed_flags >> 1) & 2)
        self.C = bool((packed_flags >> 0) & 1)

    def unconditional(self) -> bool:
        return True

    def is_overflow(self) -> bool:
        return self.V

    def is_not_overflow(self) -> bool:
        return not self.V

    def is_negative(self) -> bool:
        return self.N

    def is_not_negative(self) -> bool:
        return not self.N

    def is_equal(self) -> bool:
        return self.Z

    def is_not_equal(self) -> bool:
        return not self.Z

    # Opposite carry check from x86 due to carry semantics
    def is_carry(self) -> bool:
        return not self.C

    # Opposite carry check from x86 due to carry semantics
    def is_not_carry(self) -> bool:
        return self.C

    # Opposite carry check from x86 due to carry semantics
    def is_below_or_equal(self) -> bool:
        return not self.C or self.Z

    # Opposite carry check from x86 due to carry semantics
    def is_above(self) -> bool:
        return self.C and not self.Z

    def is_less(self) -> bool:
        return self.N != self.V

    def is_greater_or_equal(self) -> bool:
        return self.N == self.V

    def is_less_or_equal(self) -> bool:
        return self.Z or (self.N != self.V)

    def is_greater(self) -> bool:
        return not self.Z and self.N == self.V


class Mode(Enum):
    FETCH = 0
    NMI = 1
    IRQ = 2
    STALL = 3


@dataclass
class State:
    mode: Mode
    flags: Flags
    opcode: int

    @classmethod
    def from_packed(cls, packed_state: int) -> "State":
        packed_flags = (packed_state >> 0) & 0b1111
        op = (packed_state >> 4) & 0b1111_1111
        ext = (packed_state >> 12) & 0b1
        mode = (packed_state >> 13) & 0b11

        mode = Mode(mode)
        flags = Flags(packed_flags)
        opcode = op | (ext << 8)

        return cls(mode, flags, opcode)
