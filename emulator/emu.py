import random
from enum import IntEnum
from os import PathLike
from pathlib import Path
import textwrap
from typing import Callable


def mask_shift(value: int, mask: int, shift: int, to_bool: bool = False):
    result = (value & (mask << shift)) >> shift
    if to_bool:
        return bool(result)
    return result


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
    BR = 7


class AddrReg(IntEnum):
    PC = 0
    SP = 1
    X = 2
    Y = 3

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

class XferLoad(IntEnum):
    NULL = 0
    PC = 1
    SP = 2
    X = 3
    Y = 4
    AB = 5
    CD = 6

class Count(IntEnum):
    NULL = 0
    INC_PC = 1
    INC_SP = 2
    INC_X = 3
    INC_Y = 4
    INC_ADDR = 5
    DEC_X = 6
    DEC_Y = 7

class MemIO(IntEnum):
    Mem = 1
    IO = 0
class BW8cpu:
    irq_vector = 0x03
    nmi_vector = 0x06

    def __init__(
        self,
        ucode_path: PathLike,
        mem_read: Callable[[int, int], int],
        mem_write: Callable[[int, int, int], None],
        io_read: Callable[[int, int], int],
        io_write: Callable[[int, int, int], None],
    ) -> None:
        # Initialize random values within range for General Purpose
        # Registers, Internal Registers, and Address Registers
        self.gpr = [random.randint(0x00, 0xFF) for _ in GenPurpReg]
        self.inr = [random.randint(0x00, 0xFF) for _ in IntReg]
        self.adr = [random.randint(0x00, 0xFFFF) for _ in AddrReg]

        # Initialize Interrupt Lines. These should be pulled
        # high (active low signals) at startup time.
        self.irq = False
        self.nmi = False
        self.req = False

        # Initialize stateful Control Unit devices with random values
        # within appropriate ranges
        self.sequencer = random.randint(0, 7)
        self._read_ucode(ucode_path)
        self.ctrl_latch = random.randint(0x00, 0xFFFF_FFFF)
        self.ext = random.choice([True, False])

        self.mem_io = random.choice([True, False])

        self.mem_read = mem_read 
        self.mem_write = mem_write
        self.io_read = io_read
        self.io_write = io_write

        self.dbus = 0x00
        self.xfer = 0x0000
        self.addr = 0x0000

    def _read_ucode(self, path: PathLike):
        self.ucode = [0 for _ in range(2 ** 18)]

        for i in range(4):
            with open(Path(path) / f"microcode{i}.bin", "rb") as f:
                for addr, _ in enumerate(self.ucode):
                    byte = f.read(1)
                    char = int.from_bytes(byte, "big")
                    char <<= (8 * i)
                    self.ucode[addr] |= char

    @property
    def mode(self) -> CPUMode:
        if self.req:
            return CPUMode.STALL
        if self.nmi:
            return CPUMode.NMI
        if self.irq:
            return CPUMode.IRQ
        return CPUMode.FETCH

    @property
    def flags(self) -> int:
        return self.inr[IntReg.SR] & 0b0000_1111

    def reset(self) -> None:
        self.gpr = [0 for _ in GenPurpReg]
        self.inr = [0 for _ in IntReg]
        self.adr = [0 for _ in AddrReg]
        self.sequencer = 0
        self.ctrl_latch = 0
        self.ext = False
        self.mem_io = MemIO.Mem

    def rising(self) -> None:
        state = (
            self.mode << 16
            | self.ext << 15
            | self.inr[IntReg.IR] << 7
            | self.flags << 3
            | self.sequencer << 0
        )
        self.ctrl_latch = self.ucode[state]

        dbus_assert = mask_shift(self.ctrl_latch, 0b1111, 0)
        alu_op = mask_shift(self.ctrl_latch, 0b1111, 9)
        xfer_assert = mask_shift(self.ctrl_latch, 0b11111, 13)
        addr_assert = mask_shift(self.ctrl_latch, 0b111, 21)
        offset = mask_shift(self.ctrl_latch, 0b1, 30, to_bool=True)

        self.mem_io = MemIO.Mem

        match AddrAssert(addr_assert):
            case AddrAssert.ACK:
                pass
            case AddrAssert.PC:
                self.addr = self.adr[AddrReg.PC]
            case AddrAssert.SP:
                self.addr = self.adr[AddrReg.SP]
            case AddrAssert.X:
                self.addr = self.adr[AddrReg.X]
            case AddrAssert.Y:
                self.addr = self.adr[AddrReg.Y]
            case AddrAssert.DP:
                self.addr = (self.inr[IntReg.DP] << 8) | self.inr[IntReg.DA]
            case AddrAssert.T:
                self.addr = (self.inr[IntReg.TH] << 8) | self.inr[IntReg.TL] 
            case AddrAssert.IO:
                self.mem_io = MemIO.IO
                self.addr = (self.inr[IntReg.TH] << 8) | self.inr[IntReg.TL]

        match XferAssert(xfer_assert):
            case XferAssert.PC:
                self.xfer = self.adr[AddrReg.PC]
            case XferAssert.SP:
                self.xfer = self.adr[AddrReg.SP]
            case XferAssert.X:
                self.xfer = self.adr[AddrReg.X]
            case XferAssert.Y:
                self.xfer = self.adr[AddrReg.Y]
            case XferAssert.IRQ:
                self.xfer = self.irq_vector
            case XferAssert.ADDR:
                self.xfer = self.addr
                # TODO: include + offset here
            case XferAssert.A_A:
                self.xfer = (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.A]
            case XferAssert.A_B:
                self.xfer = (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.B]
            case XferAssert.A_C:
                self.xfer = (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.C]
            case XferAssert.A_D:
                self.xfer = (self.gpr[GenPurpReg.A] << 8) | self.gpr[GenPurpReg.D]
            case XferAssert.A_TL:
                self.xfer = (self.gpr[GenPurpReg.A] << 8) | self.inr[IntReg.TL]
            case XferAssert.B_A:
                self.xfer = (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.A]
            case XferAssert.B_B:
                self.xfer = (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.B]
            case XferAssert.B_C:
                self.xfer = (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.C]
            case XferAssert.B_D:
                self.xfer = (self.gpr[GenPurpReg.B] << 8) | self.gpr[GenPurpReg.D]
            case XferAssert.B_TL:
                self.xfer = (self.gpr[GenPurpReg.B] << 8) | self.inr[IntReg.TL]
            case XferAssert.C_A:
                self.xfer = (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.A]
            case XferAssert.C_B:
                self.xfer = (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.B]
            case XferAssert.C_C:
                self.xfer = (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.C]
            case XferAssert.C_D:
                self.xfer = (self.gpr[GenPurpReg.C] << 8) | self.gpr[GenPurpReg.D]
            case XferAssert.C_TL:
                self.xfer = (self.gpr[GenPurpReg.C] << 8) | self.inr[IntReg.TL]
            case XferAssert.D_A:
                self.xfer = (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.A]
            case XferAssert.D_B:
                self.xfer = (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.B]
            case XferAssert.D_C:
                self.xfer = (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.C]
            case XferAssert.D_D:
                self.xfer = (self.gpr[GenPurpReg.D] << 8) | self.gpr[GenPurpReg.D]
            case XferAssert.D_TL:
                self.xfer = (self.gpr[GenPurpReg.D] << 8) | self.inr[IntReg.TL]
            case XferAssert.TH_A:
                self.xfer = (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.A]
            case XferAssert.TH_B:
                self.xfer = (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.B]
            case XferAssert.TH_D:
                self.xfer = (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.C]
            case XferAssert.TH_D:
                self.xfer = (self.inr[IntReg.TH] << 8) | self.gpr[GenPurpReg.D]
            case XferAssert.T:
                self.xfer = (self.inr[IntReg.TH] << 8) | self.inr[IntReg.TL]
            case XferAssert.NMI:
                self.xfer = self.nmi_vector

        match DbusAssert(dbus_assert):
            case DbusAssert.ALU:
                pass
            case DbusAssert.A:
                self.dbus = self.gpr[GenPurpReg.A]
            case DbusAssert.B:
                self.dbus = self.gpr[GenPurpReg.B]
            case DbusAssert.C:
                self.dbus = self.gpr[GenPurpReg.C]
            case DbusAssert.D:
                self.dbus = self.gpr[GenPurpReg.D]
            case DbusAssert.DP:
                self.dbus = self.inr[IntReg.DP]
            case DbusAssert.DA:
                self.dbus = self.inr[IntReg.DA]
            case DbusAssert.TH:
                self.dbus = self.inr[IntReg.TH]
            case DbusAssert.TL:
                self.dbus = self.inr[IntReg.TL]
            case DbusAssert.SR:
                self.dbus = self.inr[IntReg.SR]
            case DbusAssert.MEM:
                if self.mem_io == MemIO.Mem:
                    self.dbus = self.mem_read(self.inr[IntReg.BR], self.addr)
                if self.mem_io == MemIO.IO:
                    self.dbus = self.io_read(self.inr[IntReg.BR], self.addr)
            case DbusAssert.MSB:
                self.dbus = self.mask_shift(self.xfer, 0b1111_1111, 8)
            case DbusAssert.LSB:
                self.dbus = self.xfer & 0b1111_1111
            case DbusAssert.BR:
                self.dbus = self.inr[IntReg.BR]

    def falling(self) -> None:
        # Update sequencer, load registers
        dbus_load = mask_shift(self.ctrl_latch, 0b11111, 4)
        xfer_load = mask_shift(self.ctrl_latch, 0b111, 18)
        count = mask_shift(self.ctrl_latch, 0b111, 24)
        dec_sp = mask_shift(self.ctrl_latch, 0b1, 27, to_bool=True)
        rst_useq = mask_shift(self.ctrl_latch, 0b1, 28, to_bool=True)
        tog_ext = mask_shift(self.ctrl_latch, 0b1, 29, to_bool=True)

        match DbusLoad(dbus_load):
            case DbusLoad.NULL:
                pass
            case DbusLoad.A:
                self.gpr[GenPurpReg.A] = self.dbus
            case DbusLoad.B:
                self.gpr[GenPurpReg.B] = self.dbus
            case DbusLoad.C:
                self.gpr[GenPurpReg.C] = self.dbus
            case DbusLoad.D:
                self.gpr[GenPurpReg.D] = self.dbus
            case DbusLoad.DP:
                self.inr[IntReg.DP] = self.dbus
            case DbusLoad.DA:
                self.inr[IntReg.DA] = self.dbus
            case DbusLoad.TH:
                self.inr[IntReg.TH] = self.dbus
            case DbusLoad.TL:
                self.inr[IntReg.TL] = self.dbus
            case DbusLoad.SR:
                self.inr[IntReg.SR] = self.dbus
            case DbusLoad.MEM:
                pass
            case DbusLoad.IR:
                self.inr[IntReg.IR] = self.dbus
            case DbusLoad.OFF:
                self.inr[IntReg.OF] = self.dbus
            case DbusLoad.PCH:
                pc = self.adr[AddrReg.PC]
                self.adr[AddrReg.PC] = (self.dbus << 8) | (pc & 0xff)
            case DbusLoad.PCL:
                pc = self.adr[AddrReg.PC]
                self.adr[AddrReg.PC] = (pc & (0xff << 8)) | self.dbus
            case DbusLoad.SPH:
                sp = self.adr[AddrReg.SP]
                self.adr[AddrReg.SP] = (self.dbus << 8) | (sp & 0xff)
            case DbusLoad.SPL:
                sp = self.adr[AddrReg.SP]
                self.adr[AddrReg.SP] = (sp & (0xff << 8)) | self.dbus
            case DbusLoad.XH:
                x = self.adr[AddrReg.X]
                self.adr[AddrReg.X] = (self.dbus << 8) | (x & 0xff)
            case DbusLoad.XL:
                x = self.adr[AddrReg.X]
                self.adr[AddrReg.X] = (x & (0xff << 8)) | self.dbus
            case DbusLoad.YH:
                y = self.adr[AddrReg.Y]
                self.adr[AddrReg.Y] = (self.dbus << 8) | (y & 0xff)
            case DbusLoad.YL:
                y = self.adr[AddrReg.Y]
                self.adr[AddrReg.Y] = (y & (0xff << 8)) | self.dbus
            case DbusLoad.BR:
                self.inr[IntReg.BR] = self.dbus

        match XferLoad(xfer_load):
            case XferLoad.NULL:
                pass
            case XferLoad.PC:
                self.adr[AddrReg.PC] = self.xfer
            case XferLoad.SP:
                self.adr[AddrReg.SP] = self.xfer
            case XferLoad.X:
                self.adr[AddrReg.X] = self.xfer
            case XferLoad.Y:
                self.adr[AddrReg.Y] = self.xfer
            case XferLoad.AB:
                self.gpr[GenPurpReg.A] = self.xfer >> 8
                self.gpr[GenPurpReg.B] = self.xfer & 0xff
            case XferLoad.CD:
                self.gpr[GenPurpReg.C] = self.xfer >> 8
                self.gpr[GenPurpReg.D] = self.xfer & 0xff

        match Count(count):
            case Count.NULL:
                pass
            case Count.INC_PC:
                self.adr[AddrReg.PC] += 1
                self.adr[AddrReg.PC] %= (0xffff + 1)
            case Count.INC_SP:
                self.adr[AddrReg.SP] += 1
                self.adr[AddrReg.SP] %= (0xffff + 1)
            case Count.INC_X:
                self.adr[AddrReg.X] += 1
                self.adr[AddrReg.X] %= (0xffff + 1)
            case Count.INC_Y:
                self.adr[AddrReg.Y] += 1
                self.adr[AddrReg.Y] %= (0xffff + 1)
            case Count.INC_ADDR:
                pass
            case Count.DEC_X:
                self.adr[AddrReg.X] -= 1
                if self.adr[AddrReg.X] == -1:
                    self.adr[AddrReg.X] = 0
            case Count.DEC_Y:
                self.adr[AddrReg.Y] -= 1
                if self.adr[AddrReg.Y] == -1:
                    self.adr[AddrReg.Y] = 0

        if dec_sp:
            self.adr[AddrReg.SP] -= 1
            if self.adr[AddrReg.SP] == -1:
                self.adr[AddrReg.SP] = 0

        if tog_ext:
            self.ext = 1

        self.sequencer += 1
        self.sequencer %= 8
        if rst_useq:
            self.sequencer = 0

    def clock(self) -> None:
        self.rising()
        self.falling()

    def dump(self) -> str:
        c_flag = (self.inr[IntReg.SR] & 0b1000) >> 3
        z_flag = (self.inr[IntReg.SR] & 0b0100) >> 2
        v_flag = (self.inr[IntReg.SR] & 0b0010) >> 1
        n_flag = (self.inr[IntReg.SR] & 0b0001) >> 0

        return textwrap.dedent(f"""
        BW8cpu Dump
        Registers:
            A:  {self.gpr[GenPurpReg.A]:02x}\tB:  {self.gpr[GenPurpReg.B]:02x}
            C:  {self.gpr[GenPurpReg.C]:02x}\tD:  {self.gpr[GenPurpReg.D]:02x}

            DP: {self.inr[IntReg.DP]:02x}\tDA: {self.inr[IntReg.DA]:02x}
            TH: {self.inr[IntReg.TH]:02x}\tTL: {self.inr[IntReg.TL]:02x}

            IR: {self.inr[IntReg.IR]:02x}\tOF: {self.inr[IntReg.OF]:02x}

            X:  {self.adr[AddrReg.X]:04x}\tY:  {self.adr[AddrReg.Y]:04x}
            SP: {self.adr[AddrReg.SP]:04x}\tPC: {self.adr[AddrReg.PC]:04x}

            BR: {self.inr[IntReg.BR]:04x}\tC Z V N
                        {c_flag} {z_flag} {v_flag} {n_flag}

            Tstate: {self.sequencer:01}\tMode: {self.mode.name}
        Buses:
            XFER: {self.xfer:04x}\tADDR: {self.addr:04x}
            DBUS: {self.dbus:02x}
        Interrupts:
            RST: {False}\tREQ: {self.req}
            IRQ: {self.irq}\tNMI: {self.nmi}
        """)

def mem_read(bank: int, addr: int) -> int:
    return 0x01

def mem_write(bank: int, addr: int, data: int) -> None:
    pass

def io_read(bank: int, addr: int) -> int:
    pass

def io_write(bank: int, addr: int, data: int) -> None:
    pass

def main():
    cpu = BW8cpu(
        ucode_path=Path.cwd() / ".." / "control",
        mem_read=mem_read,
        mem_write=mem_write,
        io_read=io_read,
        io_write=io_write,
    )
    cpu.reset()
    for _ in range(5):
        print(cpu.dump())
        cpu.clock()
        input()


if __name__ == "__main__":
    main()
