import random
from enum import IntEnum
from os import PathLike
from pathlib import Path


class Ctrl:
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
    DBUS_ASSERT_DPI = 11 << 0
    DBUS_ASSERT_SPIH = 12 << 0
    DBUS_ASSERT_SPIL = 13 << 0
    DBUS_ASSERT_MSB = 14 << 0
    DBUS_ASSERT_LSB = 15 << 0

    # 5 bits for DBUS Load
    DBUS_LOAD_NULL = 0 << 4
    DBUS_LOAD_A = 1 << 4
    DBUS_LOAD_B = 2 << 4
    DBUS_LOAD_C = 3 << 4
    DBUS_LOAD_D = 4 << 4
    DBUS_LOAD_DP = 5 << 4
    DBUS_LOAD_DA = 6 << 4
    DBUS_LOAD_TH = 7 << 4
    DBUS_LOAD_TL = 8 << 4
    DBUS_LOAD_SR = 9 << 4
    DBUS_LOAD_MEM = 10 << 4
    DBUS_LOAD_IR = 11 << 4
    DBUS_LOAD_OFF = 12 << 4
    DBUS_LOAD_PCH = 13 << 4
    DBUS_LOAD_PCL = 14 << 4
    DBUS_LOAD_SPH = 15 << 4
    DBUS_LOAD_SPL = 16 << 4
    DBUS_LOAD_XH = 17 << 4
    DBUS_LOAD_XL = 18 << 4
    DBUS_LOAD_YH = 19 << 4
    DBUS_LOAD_YL = 20 << 4

    # 4 bits for ALU OP
    ALU_NOP = 0 << 9
    ALU_ADC = 1 << 9
    ALU_SBC = 2 << 9
    ALU_INC = 3 << 9
    ALU_DEC = 4 << 9
    ALU_AND = 5 << 9
    ALU_OR = 6 << 9
    ALU_XOR = 7 << 9
    ALU_NOT = 8 << 9
    ALU_SRC = 9 << 9
    ALU_ASR = 10 << 9
    ALU_SEI = 11 << 9
    ALU_CLI = 12 << 9
    ALU_SEC = 13 << 9
    ALU_CLC = 14 << 9
    ALU_CLV = 15 << 9

    # 5 bits for XFER Assert
    XFER_ASSERT_PC = 0 << 13
    XFER_ASSERT_SP = 1 << 13
    XFER_ASSERT_X = 2 << 13
    XFER_ASSERT_Y = 3 << 13
    XFER_ASSERT_RST = 4 << 13
    XFER_ASSERT_ISR = 5 << 13
    XFER_ASSERT_ADDR = 6 << 13
    XFER_ASSERT_A_A = 7 << 13
    XFER_ASSERT_A_B = 8 << 13
    XFER_ASSERT_A_C = 9 << 13
    XFER_ASSERT_A_D = 10 << 13
    XFER_ASSERT_A_TL = 11 << 13
    XFER_ASSERT_B_A = 12 << 13
    XFER_ASSERT_B_B = 13 << 13
    XFER_ASSERT_B_C = 14 << 13
    XFER_ASSERT_B_D = 15 << 13
    XFER_ASSERT_B_TL = 16 << 13
    XFER_ASSERT_C_A = 17 << 13
    XFER_ASSERT_C_B = 18 << 13
    XFER_ASSERT_C_C = 19 << 13
    XFER_ASSERT_C_D = 20 << 13
    XFER_ASSERT_C_TL = 21 << 13
    XFER_ASSERT_D_A = 22 << 13
    XFER_ASSERT_D_B = 23 << 13
    XFER_ASSERT_D_C = 24 << 13
    XFER_ASSERT_D_D = 25 << 13
    XFER_ASSERT_D_TL = 26 << 13
    XFER_ASSERT_TH_A = 27 << 13
    XFER_ASSERT_TH_B = 28 << 13
    XFER_ASSERT_TH_C = 29 << 13
    XFER_ASSERT_TH_D = 30 << 13
    XFER_ASSERT_T = 31 << 13

    # 3 bits for XFER Load
    XFER_LOAD_NULL = 0 << 18
    XFER_LOAD_PC = 1 << 18
    XFER_LOAD_SP = 2 << 18
    XFER_LOAD_X = 3 << 18
    XFER_LOAD_Y = 4 << 18
    XFER_LOAD_AB = 5 << 18
    XFER_LOAD_CD = 6 << 18

    # 3 bits for ADDR Assert
    ADDR_ASSERT_ACK = 0 << 21
    ADDR_ASSERT_PC = 1 << 21
    ADDR_ASSERT_SP = 2 << 21
    ADDR_ASSERT_X = 3 << 21
    ADDR_ASSERT_Y = 4 << 21
    ADDR_ASSERT_DP = 5 << 21
    ADDR_ASSERT_T = 6 << 21

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


class GenPurpReg(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3


class IntReg(IntEnum):
    DP = 0
    DA = 1
    TH = 2
    TL = 3
    IR = 4
    SR = 5
    OF = 6


class AddrReg(IntEnum):
    PC = 0
    SP = 1
    X = 2
    Y = 3


class BW8cpu:
    DPI = 0x01
    SPI = 0xFFFF
    RSTv_Hi = 0x0100
    ISRv_Hi = 0x0000

    def __init__(self, ucode_path: PathLike) -> None:
        self.gpr = [random.randint(0x00, 0xFF) for _ in GenPurpReg]
        self.inr = [random.randint(0x00, 0xFF) for _ in IntReg]
        self.adr = [random.randint(0x00, 0xFFFF) for _ in AddrReg]
        self.rst = False
        self.irq = False
        self.sequencer = random.randint(0, 7)
        self.irq_latched = random.choice((True, False))
        self.rst_latched = random.choice((True, False))
        self.rst_sr = random.choice((True, False))
        self.ext_latched = random.choice((True, False))
        self.ctrl_latched = random.randint(0x00000000, 0xFFFFFFFF)
        self.ucode = self._read_ucode(ucode_path)

        self.dbus = 0x00
        self.xfer = 0x0000
        self.addr = 0x0000

    @staticmethod
    def _read_ucode(path: PathLike):
        normalized = Path(path)
        ucode = []
        with normalized.open("rb") as f:
            for _ in range(512 * 1024):
                ucode.append(int.from_bytes(f.read(4), "big"))
        return ucode

    def reset(self) -> None:
        self.gpr = [0 for _ in GenPurpReg]
        self.inr = [0 for _ in IntReg]
        self.adr = [0 for _ in AddrReg]
        self.rst = True
        self.irq = False
        self.sequencer = 0
        self.rst_latched = False
        self.rst_sr = True
        self.irq_latched = False
        self.ext_latched = False
        self.ctrl_latched = 0

    def interrupt(self) -> None:
        self.irq = True

    @property
    def flags(self) -> int:
        sr = self.inr[IntReg.SR]
        return sr & 0b0001_1111

    def rising(self) -> None:
        self.ctrl_latched = self.ucode[
            int(self.rst_latched) << 18
            | int(self.irq_latched) << 17
            | int(self.ext_latched) << 16
            | self.inr[IntReg.IR] << 8
            | self.flags << 3
            | self.sequencer << 0
        ]

        self._decode_ctrlword()

    def _decode_ctrlword(self):
        dbus_assert = self.ctrl_latched & (0b1111 << 0)
        dbus_load = self.ctrl_latched & (0b11111 << 4)
        alu_op = self.ctrl_latched & (0b1111 << 9)
        xfer_assert = self.ctrl_latched & (0b11111 << 13)
        xfer_load = self.ctrl_latched & (0b111 << 18)
        addr_assert = self.ctrl_latched & (0b111 << 21)
        count = self.ctrl_latched & (0b111 << 24)
        dec_sp = bool(self.ctrl_latched & (0b1 << 27))
        rst_useq = bool(self.ctrl_latched & (0b1 << 28))
        tog_ext = bool(self.ctrl_latched & (0b1 << 29))
        offset = bool(self.ctrl_latched & (0b1 << 30))
        brk_clk = bool(self.ctrl_latched & (0b1 << 31))

        self.addr = [
            0,  # ADDR_ACK
            self.adr[AddrReg.PC],
            self.adr[AddrReg.SP],
            self.adr[AddrReg.X],
            self.adr[AddrReg.Y],
            (self.inr[IntReg.DA] << 8) | self.inr[IntReg.DP],
            (self.inr[IntReg.TH] << 8) | self.inr[IntReg.TL],
            0,  # UNUSED
        ][addr_assert >> 21]

        self.xfer = [
            self.adr[AddrReg.PC],
            self.adr[AddrReg.SP],
            self.adr[AddrReg.X],
            self.adr[AddrReg.Y],
            self.RSTv_Hi,
            self.ISRv_Hi,
            self.addr,  # TODO: this needs to be the addr plus the offset
            (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.A],
            (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.B],
            (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.C],
            (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.D],
            (self.gpr[GenPurpReg.A] << 8) | self.inr[IntReg.TL],
            (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.A],
            (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.B],
            (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.C],
            (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.D],
            (self.gpr[GenPurpReg.B] << 8) | self.inr[IntReg.TL],
            (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.A],
            (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.B],
            (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.C],
            (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.D],
            (self.gpr[GenPurpReg.C] << 8) | self.inr[IntReg.TL],
            (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.A],
            (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.B],
            (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.C],
            (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.D],
            (self.gpr[GenPurpReg.D] << 8) | self.inr[IntReg.TL],
            (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.A],
            (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.B],
            (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.C],
            (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.D],
            (self.inr[IntReg.TH] << 8) | self.inr[IntReg.TL],
        ][xfer_assert >> 18]

        self.dbus = [
            0,  # dependency here. alu result needs to be known.
            self.gpr[GenPurpReg.A],
            self.gpr[GenPurpReg.B],
            self.gpr[GenPurpReg.C],
            self.gpr[GenPurpReg.D],
            self.inr[IntReg.DP],
            self.inr[IntReg.DA],
            self.inr[IntReg.TH],
            self.inr[IntReg.TL],
            self.inr[IntReg.SR],
            0,  # dependency here. membus value needs to be known.
            self.DPI,
            self.SPI >> 8,
            self.SPI & 0x00FF,
            self.xfer >> 8,
            self.xfer & 0x00FF,
        ][dbus_assert >> 0]

    def falling(self) -> None:
        # Update sequencer, irq-latched, rst-latched
        ...

    def dump(self) -> str:
        return f"""BW8cpu Dump
A: {self.gpr[GenPurpReg.A]}
B: {self.gpr[GenPurpReg.B]}
C: {self.gpr[GenPurpReg.C]}
D: {self.gpr[GenPurpReg.D]}
X: {self.adr[AddrReg.X]}
Y: {self.adr[AddrReg.Y]}
SP: {self.adr[AddrReg.SP]}
PC: {self.adr[AddrReg.PC]}
RST-latched: {self.rst_latched}
RST-sr: {self.rst_sr}
        """

def main():
    cpu = BW8cpu("ucode.bin")
    cpu.reset()

    cpu.rising()
    cpu.falling()

    print(cpu.dump())


if __name__ == "__main__":
    main()
