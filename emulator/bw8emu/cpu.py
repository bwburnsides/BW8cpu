import random
from os import PathLike
from pathlib import Path
import textwrap

from .system_bus import ISystemBus
from .cpu_enums import *


def mask_shift(value: int, mask: int, shift: int, to_bool: bool = False):
    result = (value & (mask << shift)) >> shift
    if to_bool:
        return bool(result)
    return result


class BW8cpu:
    _irq_vector = 0x03
    _nmi_vector = 0x06

    _diode_matrix = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    def __init__(
        self,
        ucode_path: PathLike,
        system_bus: ISystemBus,
    ) -> None:
        # Initialize random values within range for General Purpose
        # Registers, Internal Registers, and Address Registers
        self._gpr = [random.randint(0x00, 0xFF) for _ in GenPurpReg]
        self._inr = [random.randint(0x00, 0xFF) for _ in IntReg]
        self._adr = [random.randint(0x00, 0xFFFF) for _ in AddrReg]

        # Initialize Interrupt Lines. These should be pulled
        # high (active low signals) at startup time.
        self._irq = random.choice([True, False])
        self._nmi = random.choice([True, False])
        self._req = random.choice([True, False])
        self._rst = random.choice([True, False])

        # Initialize stateful Control Unit devices with random values
        # within appropriate ranges
        self._ucode = [0 for _ in range(256 * 1024)]
        self._read_ucode(ucode_path)
        self._sequencer = random.randint(0, 7)
        self._ctrl_latch = random.randint(0x00, 0xFFFF_FFFF)
        self._ext = random.choice([True, False])

        self._system_bus = system_bus
        self._system_bus.memory = random.choice([True, False])
        self._system_bus.read = random.choice([True, False])
        self._system_bus.supervisor = random.choice([True, False])
        self._system_bus.data = random.choice([True, False])

        self._dbus = 0
        self._xfer = 0
        self._addr = 0

        self._bank = random.randint(0x0, 0xF)

        self._resolve_dbus()
        self._resolve_xfer_bus()
        self._resolve_addr_bus()

        # Update the ALU result to be based off of these new values
        self._alu_result = 0
        self._alu_calculate()

    def reset(self, state: bool) -> None:
        self._rst = state

        if self._rst:
            self._gpr = [0 for _ in GenPurpReg]
            self._inr = [0 for _ in IntReg]
            self._adr = [0 for _ in AddrReg]
            self._sequencer = 0
            self._ctrl_latch = 0
            self._ext = False

            self._irq = False
            self._nmi = False
            self._req = False

            self._system_bus.memory = True
            self._system_bus.read = True
            self._system_bus.supervisor = True
            self._system_bus.data = True

            self._resolve_dbus()
            self._resolve_xfer_bus()
            self._resolve_addr_bus()

            self._bank = 0x00

            # Update the ALU Result to be based on these new values
            self._alu_calculate()

    def _read_ucode(self, path: PathLike):
        self._ucode = [0 for _ in range(2 ** 18)]

        for i in range(4):
            with open(Path(path) / f"microcode{i}.bin", "rb") as f:
                for addr, _ in enumerate(self._ucode):
                    byte = f.read(1)
                    char = int.from_bytes(byte, "big")
                    char <<= (8 * i)
                    self._ucode[addr] |= char

    @property
    def _mode(self) -> CPUMode:
        if self._req:
            return CPUMode.STALL
        if self._nmi:
            return CPUMode.NMI
        if self._irq:
            return CPUMode.IRQ
        return CPUMode.FETCH

    @property
    def _flags(self) -> int:
        return self._inr[IntReg.SR] & 0b0000_1111

    def request(self, state: bool) -> None:
        self._req = state

    def maskable_int(self, state: bool) -> None:
        self._irq = state

    def nonmaskable_int(self, state: bool) -> None:
        self._nmi = state

    def rising(self) -> None:
        if self._rst:
            return

        state = (
            self._mode << 16
            | self._ext << 15
            | self._inr[IntReg.IR] << 7
            | self._flags << 3
            | self._sequencer << 0
        )
        self._ctrl_latch = self._ucode[state]

        alu_op = mask_shift(self._ctrl_latch, 0b1111, 9)
        offset = mask_shift(self._ctrl_latch, 0b1, 30, to_bool=True)

        self._system_bus.memory = True

        self._resolve_addr_bus()
        self._resolve_xfer_bus()
        self._resolve_dbus()

        self._alu_calculate()

    def falling(self) -> None:
        if self._rst:
            return

        # Update sequencer, load registers
        dbus_load = mask_shift(self._ctrl_latch, 0b11111, 4)
        xfer_load = mask_shift(self._ctrl_latch, 0b111, 18)
        count = mask_shift(self._ctrl_latch, 0b111, 24)
        dec_sp = mask_shift(self._ctrl_latch, 0b1, 27, to_bool=True)
        rst_useq = mask_shift(self._ctrl_latch, 0b1, 28, to_bool=True)
        tog_ext = mask_shift(self._ctrl_latch, 0b1, 29, to_bool=True)

        self._inr[IntReg.SR] = self.alu_flags

        match DbusLoad(dbus_load):
            case DbusLoad.NULL:
                pass
            case DbusLoad.A:
                self._gpr[GenPurpReg.A] = self._dbus
            case DbusLoad.B:
                self._gpr[GenPurpReg.B] = self._dbus
            case DbusLoad.C:
                self._gpr[GenPurpReg.C] = self._dbus
            case DbusLoad.D:
                self._gpr[GenPurpReg.D] = self._dbus
            case DbusLoad.DP:
                self._inr[IntReg.DP] = self._dbus
            case DbusLoad.DA:
                self._inr[IntReg.DA] = self._dbus
            case DbusLoad.TH:
                self._inr[IntReg.TH] = self._dbus
            case DbusLoad.TL:
                self._inr[IntReg.TL] = self._dbus
            case DbusLoad.SR:
                self._inr[IntReg.SR] = self._dbus
            case DbusLoad.MEM:
                pass
            case DbusLoad.IR:
                self._inr[IntReg.IR] = self._dbus
            case DbusLoad.OFF:
                self._inr[IntReg.OF] = self._dbus
            case DbusLoad.PCH:
                pc = self._adr[AddrReg.PC]
                self._adr[AddrReg.PC] = (self._dbus << 8) | (pc & 0xff)
            case DbusLoad.PCL:
                pc = self._adr[AddrReg.PC]
                self._adr[AddrReg.PC] = (pc & (0xff << 8)) | self._dbus
            case DbusLoad.SPH:
                sp = self._adr[AddrReg.SP]
                self._adr[AddrReg.SP] = (self._dbus << 8) | (sp & 0xff)
            case DbusLoad.SPL:
                sp = self._adr[AddrReg.SP]
                self._adr[AddrReg.SP] = (sp & (0xff << 8)) | self._dbus
            case DbusLoad.XH:
                x = self._adr[AddrReg.X]
                self._adr[AddrReg.X] = (self._dbus << 8) | (x & 0xff)
            case DbusLoad.XL:
                x = self._adr[AddrReg.X]
                self._adr[AddrReg.X] = (x & (0xff << 8)) | self._dbus
            case DbusLoad.YH:
                y = self._adr[AddrReg.Y]
                self._adr[AddrReg.Y] = (self._dbus << 8) | (y & 0xff)
            case DbusLoad.YL:
                y = self._adr[AddrReg.Y]
                self._adr[AddrReg.Y] = (y & (0xff << 8)) | self._dbus
            case DbusLoad.BR:
                self._inr[IntReg.BR] = self._dbus

        match XferLoad(xfer_load):
            case XferLoad.NULL:
                pass
            case XferLoad.PC:
                self._adr[AddrReg.PC] = self._xfer
            case XferLoad.SP:
                self._adr[AddrReg.SP] = self._xfer
            case XferLoad.X:
                self._adr[AddrReg.X] = self._xfer
            case XferLoad.Y:
                self._adr[AddrReg.Y] = self._xfer
            case XferLoad.AB:
                self._gpr[GenPurpReg.A] = self._xfer >> 8
                self._gpr[GenPurpReg.B] = self._xfer & 0xff
            case XferLoad.CD:
                self._gpr[GenPurpReg.C] = self._xfer >> 8
                self._gpr[GenPurpReg.D] = self._xfer & 0xff

        match Count(count):
            case Count.NULL:
                pass
            case Count.INC_PC:
                self._adr[AddrReg.PC] += 1
                self._adr[AddrReg.PC] %= (0xffff + 1)
            case Count.INC_SP:
                self._adr[AddrReg.SP] += 1
                self._adr[AddrReg.SP] %= (0xffff + 1)
            case Count.INC_X:
                self._adr[AddrReg.X] += 1
                self._adr[AddrReg.X] %= (0xffff + 1)
            case Count.INC_Y:
                self._adr[AddrReg.Y] += 1
                self._adr[AddrReg.Y] %= (0xffff + 1)
            case Count.INC_ADDR:
                pass
            case Count.DEC_X:
                self._adr[AddrReg.X] -= 1
                if self._adr[AddrReg.X] == -1:
                    self._adr[AddrReg.X] = 0
            case Count.DEC_Y:
                self._adr[AddrReg.Y] -= 1
                if self._adr[AddrReg.Y] == -1:
                    self._adr[AddrReg.Y] = 0

        if dec_sp:
            self._adr[AddrReg.SP] -= 1
            if self._adr[AddrReg.SP] == -1:
                self._adr[AddrReg.SP] = 0

        if tog_ext:
            self.ext = 1

        self._sequencer += 1
        self._sequencer %= 8
        if rst_useq:
            self._sequencer = 0

    def _resolve_addr_bus(self):
        addr_assert = mask_shift(self._ctrl_latch, 0b111, 21)

        match AddrAssert(addr_assert):
            case AddrAssert.ACK:
                pass
            case AddrAssert.PC:
                self._addr = self._adr[AddrReg.PC]
            case AddrAssert.SP:
                self._addr = self._adr[AddrReg.SP]
            case AddrAssert.X:
                self._addr = self._adr[AddrReg.X]
            case AddrAssert.Y:
                self._addr = self._adr[AddrReg.Y]
            case AddrAssert.DP:
                self._addr = (self._inr[IntReg.DP] << 8) | self._inr[IntReg.DA]
            case AddrAssert.T:
                self._addr = (self._inr[IntReg.TH] << 8) | self._inr[IntReg.TL] 
            case AddrAssert.IO:
                self._system_bus.io = True
                self._addr = (self._inr[IntReg.TH] << 8) | self._inr[IntReg.TL]

    def _resolve_xfer_bus(self):
        xfer_assert = mask_shift(self._ctrl_latch, 0b11111, 13)

        match XferAssert(xfer_assert):
            case XferAssert.PC:
                self._xfer = self._adr[AddrReg.PC]
            case XferAssert.SP:
                self._xfer = self._adr[AddrReg.SP]
            case XferAssert.X:
                self._xfer = self._adr[AddrReg.X]
            case XferAssert.Y:
                self._xfer = self._adr[AddrReg.Y]
            case XferAssert.IRQ:
                self._xfer = self._irq_vector
            case XferAssert.ADDR:
                self._xfer = self._addr
                # TODO: include + offset here
            case XferAssert.A_A:
                self._xfer = (self._gpr[GenPurpReg.A] << 8) | self._gpr[GenPurpReg.A]
            case XferAssert.A_B:
                self._xfer = (self._gpr[GenPurpReg.A] << 8) | self._gpr[GenPurpReg.B]
            case XferAssert.A_C:
                self._xfer = (self._gpr[GenPurpReg.A] << 8) | self._gpr[GenPurpReg.C]
            case XferAssert.A_D:
                self._xfer = (self._gpr[GenPurpReg.A] << 8) | self._gpr[GenPurpReg.D]
            case XferAssert.A_TL:
                self._xfer = (self._gpr[GenPurpReg.A] << 8) | self._inr[IntReg.TL]
            case XferAssert.B_A:
                self._xfer = (self._gpr[GenPurpReg.B] << 8) | self._gpr[GenPurpReg.A]
            case XferAssert.B_B:
                self._xfer = (self._gpr[GenPurpReg.B] << 8) | self._gpr[GenPurpReg.B]
            case XferAssert.B_C:
                self._xfer = (self._gpr[GenPurpReg.B] << 8) | self._gpr[GenPurpReg.C]
            case XferAssert.B_D:
                self._xfer = (self._gpr[GenPurpReg.B] << 8) | self._gpr[GenPurpReg.D]
            case XferAssert.B_TL:
                self._xfer = (self._gpr[GenPurpReg.B] << 8) | self._inr[IntReg.TL]
            case XferAssert.C_A:
                self._xfer = (self._gpr[GenPurpReg.C] << 8) | self._gpr[GenPurpReg.A]
            case XferAssert.C_B:
                self._xfer = (self._gpr[GenPurpReg.C] << 8) | self._gpr[GenPurpReg.B]
            case XferAssert.C_C:
                self._xfer = (self._gpr[GenPurpReg.C] << 8) | self._gpr[GenPurpReg.C]
            case XferAssert.C_D:
                self._xfer = (self._gpr[GenPurpReg.C] << 8) | self._gpr[GenPurpReg.D]
            case XferAssert.C_TL:
                self._xfer = (self._gpr[GenPurpReg.C] << 8) | self._inr[IntReg.TL]
            case XferAssert.D_A:
                self._xfer = (self._gpr[GenPurpReg.D] << 8) | self._gpr[GenPurpReg.A]
            case XferAssert.D_B:
                self._xfer = (self._gpr[GenPurpReg.D] << 8) | self._gpr[GenPurpReg.B]
            case XferAssert.D_C:
                self._xfer = (self._gpr[GenPurpReg.D] << 8) | self._gpr[GenPurpReg.C]
            case XferAssert.D_D:
                self._xfer = (self._gpr[GenPurpReg.D] << 8) | self._gpr[GenPurpReg.D]
            case XferAssert.D_TL:
                self._xfer = (self._gpr[GenPurpReg.D] << 8) | self._inr[IntReg.TL]
            case XferAssert.TH_A:
                self._xfer = (self._inr[IntReg.TH] << 8) | self._gpr[GenPurpReg.A]
            case XferAssert.TH_B:
                self._xfer = (self._inr[IntReg.TH] << 8) | self._gpr[GenPurpReg.B]
            case XferAssert.TH_D:
                self._xfer = (self._inr[IntReg.TH] << 8) | self._gpr[GenPurpReg.C]
            case XferAssert.TH_D:
                self._xfer = (self._inr[IntReg.TH] << 8) | self._gpr[GenPurpReg.D]
            case XferAssert.T:
                self._xfer = (self._inr[IntReg.TH] << 8) | self._inr[IntReg.TL]
            case XferAssert.NMI:
                self._xfer = self._nmi_vector

    def _resolve_dbus(self):
        dbus_assert = mask_shift(self._ctrl_latch, 0b1111, 0)

        match DbusAssert(dbus_assert):
            case DbusAssert.ALU:
                pass
            case DbusAssert.A:
                self._dbus = self._gpr[GenPurpReg.A]
            case DbusAssert.B:
                self._dbus = self._gpr[GenPurpReg.B]
            case DbusAssert.C:
                self._dbus = self._gpr[GenPurpReg.C]
            case DbusAssert.D:
                self._dbus = self._gpr[GenPurpReg.D]
            case DbusAssert.DP:
                self._dbus = self._inr[IntReg.DP]
            case DbusAssert.DA:
                self._dbus = self._inr[IntReg.DA]
            case DbusAssert.TH:
                self._dbus = self._inr[IntReg.TH]
            case DbusAssert.TL:
                self._dbus = self._inr[IntReg.TL]
            case DbusAssert.SR:
                self._dbus = self._inr[IntReg.SR]
            case DbusAssert.MEM:
                self._dbus = self._system_bus.data_bus
            case DbusAssert.MSB:
                self._dbus = mask_shift(self._xfer, 0b1111_1111, 8)
            case DbusAssert.LSB:
                self._dbus = self._xfer & 0b1111_1111
            case DbusAssert.BR:
                self._dbus = self._inr[IntReg.BR]

    def _alu_calculate(self) -> None:
        alu_op = mask_shift(self._ctrl_latch, 0b1111, 9)
        alu_ctrl = self._diode_matrix[alu_op]

        sum_func = alu_ctrl & 0b11
        shift_func = mask_shift(alu_ctrl, 0b11, 2)
        logic_func = mask_shift(alu_ctrl, 0b1111, 4)

        cf_func = mask_shift(alu_ctrl, 0b111, 8)
        zf_func = mask_shift(alu_ctrl, 0b11, 11)
        vf_func = mask_shift(alu_ctrl, 0b11, 13)
        nf_func = mask_shift(alu_ctrl, 0b11, 15)
        if_func = mask_shift(alu_ctrl, 0b11, 17)

        lhs = mask_shift(self._xfer, 0xff, 8)
        rhs = self._xfer & 0xff

        sum_left = 0
        sum_right = 0
        self.alu_result = 0
        self.alu_flags = 0

        i_f = (self._inr[IntReg.SR] & 0b10000) >> 4
        c_f = (self._inr[IntReg.SR] & 0b01000) >> 3
        z_f = (self._inr[IntReg.SR] & 0b00100) >> 2
        v_f = (self._inr[IntReg.SR] & 0b00010) >> 1
        n_f = (self._inr[IntReg.SR] & 0b00001) >> 0

        c_shift = 0
        c_sum = 0

        match ALULogicFunc(logic_func):
            case ALULogicFunc.ZERO:
                sum_right = 0
            case ALULogicFunc.MAX:
                sum_right = 0xff
            case ALULogicFunc.LHS:
                sum_right = lhs
            case ALULogicFunc.RHS:
                sum_right = rhs
            case ALULogicFunc.notLHS:
                sum_right = -lhs & 0xff
            case ALULogicFunc.notRHS:
                sum_right = -rhs & 0xff
            case ALULogicFunc.OR:
                sum_right = lhs | rhs
            case ALULogicFunc.AND:
                sum_right = lhs & rhs
            case ALULogicFunc.XOR:
                sum_right = lhs ^ rhs

        match ALUShiftFunc(shift_func):
            case ALUShiftFunc.LHS:
                sum_left = lhs
            case ALUShiftFunc.ZERO:
                sum_left = 0
            case ALUShiftFunc.SRC:
                shift = lhs >> 1
                c_shift = lhs & 1
                sum_left = shift & (c_f << 7)
            case ALUShiftFunc.ASR:
                shift = lhs >> 1
                c_shift = lhs & 1
                lhs_sign = (lhs & 0b10000000) >> 7
                sum_left = shift
                if lhs_sign:
                    sum_left &= 0b10000000

        match ALUSumFunc(sum_func):
            case ALUSumFunc.ZERO:
                alu_sum = sum_left + sum_right + 0
            case ALUSumFunc.Cf:
                alu_sum = sum_left + sum_right + c_f
            case ALUSumFunc.ONE:
                alu_sum = sum_left + sum_right + 1

        if alu_sum > 0xff:
            c_sum = 1

        self.alu_result = alu_sum % 0xff

        # Calculate the new Z, V, N flags
        z = 0
        v = 0
        n = 0

        if not self.alu_result:
            z = 1

        left_sign = mask_shift(sum_left, 1, 7)
        right_sign = mask_shift(sum_right, 1, 7)
        sum_sign = mask_shift(self.alu_result, 1, 7)

        if (left_sign and right_sign) and (sum_sign != left_sign):
            v = 1

        if sum_sign:
            n = 1

        match CfFunc(cf_func):
            case CfFunc.SET:
                c_out = 1
            case CfFunc.C_SHIFT:
                c_out = c_shift
            case CfFunc.C_SUM:
                c_out = c_sum
            case CfFunc.CLEAR:
                c_out = 0
            case CfFunc.NO_CHANGE:
                c_out = c_f

        match ZfFunc(zf_func):
            case ZfFunc.SET:
                z_out = 1
            case ZfFunc.NEW:
                z_out = z
            case ZfFunc.CLEAR:
                z_out = 0
            case ZfFunc.NO_CHANGE:
                z_out = z_f

        match VfFunc(vf_func):
            case VfFunc.SET:
                v_out = 1
            case VfFunc.NEW:
                v_out = z
            case VfFunc.CLEAR:
                v_out = 0
            case VfFunc.NO_CHANGE:
                v_out = v_f

        match NfFunc(nf_func):
            case NfFunc.SET:
                n_out = 1
            case NfFunc.NEW:
                n_out = z
            case NfFunc.CLEAR:
                n_out = 0
            case NfFunc.NO_CHANGE:
                n_out = n_f

        match IfFunc(if_func):
            case IfFunc.SET:
                i_out = 1
            case IfFunc.CLEAR:
                i_out = 0
            case IfFunc.NO_CHANGE:
                i_out = i_f

        self.alu_flags = (
            n_out &
            (v_out << 1) &
            (z_out << 2) &
            (c_out << 3) &
            (i_out << 4)
        )

    def clock(self) -> None:
        self.rising()
        self.falling()

    def dump(self) -> str:
        c_flag = (self._inr[IntReg.SR] & 0b1000) >> 3
        z_flag = (self._inr[IntReg.SR] & 0b0100) >> 2
        v_flag = (self._inr[IntReg.SR] & 0b0010) >> 1
        n_flag = (self._inr[IntReg.SR] & 0b0001) >> 0

        return textwrap.dedent(f"""
        BW8cpu Dump
        Registers:
            A:  {self._gpr[GenPurpReg.A]:02x}\tB:  {self._gpr[GenPurpReg.B]:02x}
            C:  {self._gpr[GenPurpReg.C]:02x}\tD:  {self._gpr[GenPurpReg.D]:02x}

            DP: {self._inr[IntReg.DP]:02x}\tDA: {self._inr[IntReg.DA]:02x}
            TH: {self._inr[IntReg.TH]:02x}\tTL: {self._inr[IntReg.TL]:02x}

            IR: {self._inr[IntReg.IR]:02x}\tOF: {self._inr[IntReg.OF]:02x}

            X:  {self._adr[AddrReg.X]:04x}\tY:  {self._adr[AddrReg.Y]:04x}
            SP: {self._adr[AddrReg.SP]:04x}\tPC: {self._adr[AddrReg.PC]:04x}

            BR: {self._inr[IntReg.BR]:04x}\tC Z V N
                        {c_flag} {z_flag} {v_flag} {n_flag}

            Tstate: {self._sequencer:01}\tMode: {self._mode.name}

        Buses:
            XFER: {self._xfer:04x}\tADDR: {self._addr:04x}
            DBUS: {self._dbus:02x}

        Interrupts:
            RST: {self._rst}\tREQ: {self._req}
            IRQ: {self._irq}\tNMI: {self._nmi}
        """)
