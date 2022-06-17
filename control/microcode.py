from enum import Enum
from typing import Callable, Final

from .control import Ctrl, Mode, State
from .opcodes import Op

from pathlib import Path

OUTPUT_LOCATION: Final[Path] = Path(__file__) / ".." / "bin"


class GPR(Enum):
    A = (
        Ctrl.DBUS_LOAD_A,
        Ctrl.DBUS_ASSERT_A,
        Ctrl.XFER_ASSERT_A_TL,
        Ctrl.XFER_ASSERT_TH_A,
        {
            "A": Ctrl.XFER_ASSERT_A_A,
            "B": Ctrl.XFER_ASSERT_A_B,
            "C": Ctrl.XFER_ASSERT_A_C,
            "D": Ctrl.XFER_ASSERT_A_D,
        },
    )
    B = (
        Ctrl.DBUS_LOAD_B,
        Ctrl.DBUS_ASSERT_B,
        Ctrl.XFER_ASSERT_B_TL,
        Ctrl.XFER_ASSERT_TH_B,
        {
            "A": Ctrl.XFER_ASSERT_B_A,
            "B": Ctrl.XFER_ASSERT_B_B,
            "C": Ctrl.XFER_ASSERT_B_C,
            "D": Ctrl.XFER_ASSERT_B_D,
        },
    )
    C = (
        Ctrl.DBUS_LOAD_C,
        Ctrl.DBUS_ASSERT_C,
        Ctrl.XFER_ASSERT_C_TL,
        Ctrl.XFER_ASSERT_TH_C,
        {
            "A": Ctrl.XFER_ASSERT_C_A,
            "B": Ctrl.XFER_ASSERT_C_B,
            "C": Ctrl.XFER_ASSERT_C_C,
            "D": Ctrl.XFER_ASSERT_C_D,
        },
    )
    D = (
        Ctrl.DBUS_LOAD_D,
        Ctrl.DBUS_ASSERT_D,
        Ctrl.XFER_ASSERT_D_TL,
        Ctrl.XFER_ASSERT_TH_D,
        {
            "A": Ctrl.XFER_ASSERT_D_A,
            "B": Ctrl.XFER_ASSERT_D_B,
            "C": Ctrl.XFER_ASSERT_D_C,
            "D": Ctrl.XFER_ASSERT_D_D,
        },
    )

    def __init__(
        self,
        dbus_load: int,
        dbus_assert: int,
        xfer_assert_tl: int,
        xfer_assert_th: int,
        xfer_assert_gpr: dict[str, int],
    ):
        self.DBUS_LOAD = dbus_load
        self.DBUS_ASSERT = dbus_assert
        self.XFER_ASSERT_TL = xfer_assert_tl
        self.XFER_ASSERT_TH = xfer_assert_th
        self.XFER_assert_gpr = xfer_assert_gpr

    def xfer_assert(self, rhs: "GPR") -> int:
        return self.XFER_assert_gpr[rhs.name]


class MOV16(Enum):
    X = Ctrl.XFER_LOAD_X, Ctrl.XFER_ASSERT_X
    Y = Ctrl.XFER_LOAD_Y, Ctrl.XFER_ASSERT_Y

    def __init__(self, xfer_load: int, xfer_assert: int):
        self.XFER_LOAD = xfer_load
        self.XFER_ASSERT = xfer_assert


class GPP(Enum):
    X = (
        Ctrl.XFER_LOAD_X,
        Ctrl.XFER_ASSERT_X,
        Ctrl.ADDR_ASSERT_X,
        Ctrl.DBUS_LOAD_XH,
        Ctrl.DBUS_LOAD_XL,
    )
    Y = (
        Ctrl.XFER_LOAD_Y,
        Ctrl.XFER_ASSERT_Y,
        Ctrl.ADDR_ASSERT_Y,
        Ctrl.DBUS_LOAD_YH,
        Ctrl.DBUS_LOAD_YL,
    )

    def __init__(
        self,
        xfer_load: int,
        xfer_assert: int,
        addr_assert: int,
        dbus_load_hi: int,
        dbus_load_lo: int,
    ):
        self.XFER_LOAD = xfer_load
        self.XFER_ASSERT = xfer_assert
        self.ADDR_ASSERT = addr_assert
        self.DBUS_LOAD_HI = dbus_load_hi
        self.DBUS_LOAD_LO = dbus_load_lo


class PTR(Enum):
    X = Ctrl.ADDR_ASSERT_X, Ctrl.XFER_LOAD_X
    Y = Ctrl.ADDR_ASSERT_Y, Ctrl.XFER_LOAD_Y
    SP = Ctrl.ADDR_ASSERT_SP, Ctrl.XFER_LOAD_SP

    def __init__(self, addr_assert: int, xfer_load: int):
        self.ADDR_ASSERT = addr_assert
        self.XFER_LOAD = xfer_load


class BinOp(Enum):
    ADC = Ctrl.ALU_ADC
    SBC = Ctrl.ALU_SBC
    AND = Ctrl.ALU_AND
    OR = Ctrl.ALU_OR
    XOR = Ctrl.ALU_XOR


class ALUSide(Enum):
    LogicUnit = 0
    ShiftUnit = 1


class UnyOp(Enum):
    NOT = Ctrl.ALU_NOT, ALUSide.LogicUnit
    SRC = Ctrl.ALU_SRC, ALUSide.ShiftUnit
    ASR = Ctrl.ALU_ASR, ALUSide.ShiftUnit
    INC = Ctrl.ALU_INC, ALUSide.LogicUnit
    DEC = Ctrl.ALU_DEC, ALUSide.LogicUnit

    def __init__(self, alu_op: int, alu_side: ALUSide):
        self.ALU_OP = alu_op
        self.ALU_SIDE = alu_side


class StackOperable8(Enum):
    A = Ctrl.DBUS_LOAD_A, Ctrl.DBUS_ASSERT_A
    B = Ctrl.DBUS_LOAD_B, Ctrl.DBUS_ASSERT_B
    C = Ctrl.DBUS_LOAD_C, Ctrl.DBUS_ASSERT_C
    D = Ctrl.DBUS_LOAD_D, Ctrl.DBUS_ASSERT_D
    SR = Ctrl.DBUS_LOAD_SR, Ctrl.DBUS_ASSERT_SR

    def __init__(self, dbus_load: int, dbus_assert: int):
        self.DBUS_LOAD = dbus_load
        self.DBUS_ASSERT = dbus_assert


class StackOperable16(Enum):
    X = Ctrl.XFER_ASSERT_X, Ctrl.DBUS_LOAD_XH, Ctrl.DBUS_LOAD_XL
    Y = Ctrl.XFER_ASSERT_Y, Ctrl.DBUS_LOAD_YH, Ctrl.DBUS_LOAD_YL

    def __init__(self, xfer_assert: int, dbus_load_hi: int, dbus_load_lo: int):
        self.XFER_ASSERT = xfer_assert
        self.DBUS_LOAD_HI = dbus_load_hi
        self.DBUS_LOAD_LO = dbus_load_lo


FETCH = (
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_IR | Ctrl.COUNT_INC_PC
)
BASE = [FETCH, 0, 0, 0, 0, 0, 0, 0]

STALL_OPS = [Ctrl.ADDR_ASSERT_ACK for _ in range(8)]

IRQ_ACK = [
    Ctrl.COUNT_DEC_SP | Ctrl.ALU_CLI,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_SR | Ctrl.COUNT_DEC_SP,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_LSB | Ctrl.XFER_ASSERT_PC | Ctrl.COUNT_DEC_SP,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_MSB | Ctrl.XFER_ASSERT_PC | Ctrl.CTRL_SET_SUP,
    Ctrl.XFER_ASSERT_INT | Ctrl.XFER_LOAD_PC | Ctrl.CTRL_RST_USEQ,
    0, 0, 0
]

NMI_ACK = [
    Ctrl.COUNT_DEC_SP | Ctrl.ALU_CLI,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_SR | Ctrl.COUNT_DEC_SP,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_LSB | Ctrl.XFER_ASSERT_PC | Ctrl.COUNT_DEC_SP | Ctrl.CTRL_SET_NMI_MASK,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_MSB | Ctrl.XFER_ASSERT_PC | Ctrl.CTRL_SET_SUP,
    Ctrl.XFER_ASSERT_INT | Ctrl.XFER_LOAD_PC | Ctrl.CTRL_RST_USEQ,
    0, 0, 0
]

def mov8(dst: GPR, src: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= dst.DBUS_LOAD | src.DBUS_ASSERT | Ctrl.CTRL_RST_USEQ
    return uops


def in_gpr(dst: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_PORT
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_IO | Ctrl.DBUS_ASSERT_MEM | dst.DBUS_LOAD | Ctrl.CTRL_RST_USEQ
    )

    return uops


def out_gpr(src: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_PORT
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_IO | Ctrl.DBUS_LOAD_MEM | src.DBUS_ASSERT | Ctrl.CTRL_RST_USEQ
    )

    return uops


def load8_imm(dst: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.COUNT_INC_PC
        | dst.DBUS_LOAD
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def load8_abs(dst: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TH
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
    )
    uops[3] |= Ctrl.ADDR_ASSERT_T | Ctrl.DBUS_ASSERT_MEM | dst.DBUS_LOAD | Ctrl.CTRL_RST_USEQ
    return uops


def load8_dp(dst: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | dst.DBUS_LOAD | Ctrl.CTRL_RST_USEQ
    )
    return uops


def load8_ptr_idx(dst: GPR, ptr: PTR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_OFF
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        ptr.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.DBUS_ASSERT_MEM
        | dst.DBUS_LOAD
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def load8_ptr_gpr(dst: GPR, ptr: PTR, idx: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= idx.DBUS_ASSERT | Ctrl.DBUS_LOAD_OFF
    uops[2] |= (
        ptr.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.DBUS_ASSERT_MEM
        | dst.DBUS_LOAD
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def store8_abs(src: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TH
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
    )
    uops[3] |= Ctrl.ADDR_ASSERT_T | Ctrl.DBUS_LOAD_MEM | src.DBUS_ASSERT | Ctrl.CTRL_RST_USEQ
    return uops


def store8_dp(src: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_LOAD_MEM | src.DBUS_ASSERT | Ctrl.CTRL_RST_USEQ
    )
    return uops


def store8_ptr_idx(src: GPR, ptr: PTR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_OFF
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        ptr.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.DBUS_LOAD_MEM
        | src.DBUS_ASSERT
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def store8_ptr_gpr(src: GPR, ptr: PTR, idx: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= idx.DBUS_ASSERT | Ctrl.DBUS_LOAD_OFF
    uops[2] |= (
        ptr.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.DBUS_LOAD_MEM
        | src.DBUS_ASSERT
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def mov16(dst: MOV16, src: MOV16) -> list[int]:
    uops = BASE.copy()

    uops[1] |= dst.XFER_LOAD | src.XFER_ASSERT | Ctrl.CTRL_RST_USEQ
    return uops


def load16_imm(dst: GPP) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | dst.DBUS_LOAD_HI
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | dst.DBUS_LOAD_LO
        | Ctrl.COUNT_INC_PC
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def load16_abs(dst: GPP) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TH
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
    )
    uops[3] |= Ctrl.ADDR_ASSERT_T | Ctrl.DBUS_ASSERT_MEM | dst.DBUS_LOAD_HI
    uops[4] |= (
        Ctrl.ADDR_ASSERT_T
        | Ctrl.COUNT_INC_ADDR
        | Ctrl.DBUS_ASSERT_MEM
        | dst.DBUS_LOAD_LO
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def load16_dp(dst: GPP) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | dst.DBUS_LOAD_HI
    uops[3] |= (
        Ctrl.ADDR_ASSERT_DP
        | Ctrl.COUNT_INC_ADDR
        | Ctrl.DBUS_ASSERT_MEM
        | dst.DBUS_LOAD_LO
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def load16_ptr_idx(dst: GPP, ptr: PTR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_OFF
        | Ctrl.COUNT_INC_PC
    )

    if (dst == GPP.X and ptr == PTR.X) or (dst == GPP.Y and ptr == PTR.Y):
        uops[2] |= (
            ptr.ADDR_ASSERT | Ctrl.OFFSET_EN | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
        )
        uops[3] |= (
            ptr.ADDR_ASSERT
            | Ctrl.OFFSET_EN
            | Ctrl.COUNT_INC_ADDR
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_TL
        )
        uops[4] |= Ctrl.XFER_ASSERT_T | dst.XFER_LOAD | Ctrl.CTRL_RST_USEQ
    else:
        uops[2] |= (
            ptr.ADDR_ASSERT | Ctrl.OFFSET_EN | Ctrl.DBUS_ASSERT_MEM | dst.DBUS_LOAD_HI
        )
        uops[3] |= (
            ptr.ADDR_ASSERT
            | Ctrl.OFFSET_EN
            | Ctrl.COUNT_INC_ADDR
            | Ctrl.DBUS_ASSERT_MEM
            | dst.DBUS_LOAD_LO
            | Ctrl.CTRL_RST_USEQ
        )

    return uops


def store16_abs(src: GPP) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TH
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
    )
    uops[3] |= (
        Ctrl.ADDR_ASSERT_T | Ctrl.DBUS_LOAD_MEM | src.XFER_ASSERT | Ctrl.DBUS_ASSERT_MSB
    )
    uops[4] |= (
        Ctrl.ADDR_ASSERT_T
        | Ctrl.COUNT_INC_ADDR
        | Ctrl.DBUS_LOAD_MEM
        | src.XFER_ASSERT
        | Ctrl.DBUS_ASSERT_LSB
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def store16_dp(src: GPP) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_DP
        | Ctrl.DBUS_LOAD_MEM
        | src.XFER_ASSERT
        | Ctrl.DBUS_ASSERT_MSB
    )
    uops[3] |= (
        Ctrl.ADDR_ASSERT_DP
        | Ctrl.COUNT_INC_ADDR
        | Ctrl.DBUS_LOAD_MEM
        | src.XFER_ASSERT
        | Ctrl.DBUS_ASSERT_LSB
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def store16_ptr_idx(src: GPP, ptr: PTR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_OFF
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        ptr.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.DBUS_LOAD_MEM
        | src.XFER_ASSERT
        | Ctrl.DBUS_ASSERT_MSB
    )
    uops[3] |= (
        ptr.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.COUNT_INC_ADDR
        | Ctrl.DBUS_LOAD_MEM
        | src.XFER_ASSERT
        | Ctrl.DBUS_ASSERT_LSB
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def lea_gpr(dst: PTR, gpr: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= gpr.DBUS_ASSERT | Ctrl.DBUS_LOAD_OFF
    uops[2] |= (
        dst.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.XFER_ASSERT_ADDR
        | dst.XFER_LOAD
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def lea_idx(dst: PTR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_OFF
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        dst.ADDR_ASSERT
        | Ctrl.OFFSET_EN
        | Ctrl.XFER_ASSERT_ADDR
        | dst.XFER_LOAD
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def binop_gpr_gpr(op: BinOp, lhs: GPR, rhs: GPR) -> list[int]:
    uops = BASE.copy()
    XFER_ASSERT = lhs.xfer_assert(rhs)

    uops[1] |= (
        op.value | XFER_ASSERT | Ctrl.DBUS_ASSERT_ALU | lhs.DBUS_LOAD | Ctrl.CTRL_RST_USEQ
    )
    return uops


def binop_gpr_imm(op: BinOp, lhs: GPR) -> list[int]:
    uops = BASE.copy()
    XFER_ASSERT = lhs.XFER_ASSERT_TL

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        op.value | XFER_ASSERT | Ctrl.DBUS_ASSERT_ALU | lhs.DBUS_LOAD | Ctrl.CTRL_RST_USEQ
    )
    return uops


def binop_gpr_dp(op: BinOp, lhs: GPR) -> list[int]:
    uops = BASE.copy()
    XFER_ASSERT = lhs.XFER_ASSERT_TL

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL
    uops[3] |= (
        op.value | XFER_ASSERT | Ctrl.DBUS_ASSERT_ALU | lhs.DBUS_LOAD | Ctrl.CTRL_RST_USEQ
    )
    return uops


def binop_dp_gpr(op: BinOp, rhs: GPR) -> list[int]:
    uops = BASE.copy()
    XFER_ASSERT = rhs.XFER_ASSERT_TH

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
    uops[3] |= op.value | XFER_ASSERT | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TH
    uops[4] |= (
        Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_TH | Ctrl.CTRL_RST_USEQ
    )
    return uops


def binop_dp_imm(op: BinOp) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
    )
    uops[3] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
    uops[4] |= op.value | Ctrl.XFER_ASSERT_T | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TH
    uops[5] |= (
        Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_TH | Ctrl.CTRL_RST_USEQ
    )
    return uops


def unyop_gpr(op: UnyOp, reg: GPR) -> list[int]:
    uops = BASE.copy()

    if op.ALU_SIDE == ALUSide.LogicUnit:
        XFER_ASSERT = reg.XFER_ASSERT_TH
    else:  # op.ALU_SIDE == ALUSide.ShiftUnit
        XFER_ASSERT = reg.XFER_ASSERT_TL

    uops[1] |= (
        op.ALU_OP | XFER_ASSERT | Ctrl.DBUS_ASSERT_ALU | reg.DBUS_LOAD | Ctrl.CTRL_RST_USEQ
    )
    return uops


def unyop_dp(op: UnyOp) -> list[int]:
    uops = BASE.copy()

    if op.ALU_SIDE == ALUSide.LogicUnit:
        DBUS_ASSERT = Ctrl.DBUS_ASSERT_TL
        DBUS_LOAD = Ctrl.DBUS_LOAD_TL
    else:  # op.ALU_SIDE == ALUSide.ShiftUnit
        DBUS_ASSERT = Ctrl.DBUS_ASSERT_TH
        DBUS_LOAD = Ctrl.DBUS_LOAD_TH

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | DBUS_LOAD
    uops[3] |= op.ALU_OP | Ctrl.XFER_ASSERT_T | Ctrl.DBUS_ASSERT_ALU | DBUS_LOAD
    uops[4] |= Ctrl.DBUS_ASSERT_DP | Ctrl.DBUS_LOAD_MEM | DBUS_ASSERT | Ctrl.CTRL_RST_USEQ
    return uops


def neg_gpr(reg: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= Ctrl.ALU_NOT | reg.XFER_ASSERT_TH | Ctrl.DBUS_ASSERT_ALU | reg.DBUS_LOAD
    uops[2] |= (
        Ctrl.ALU_INC
        | reg.XFER_ASSERT_TH
        | Ctrl.DBUS_ASSERT_ALU
        | reg.DBUS_LOAD
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def push8(reg: StackOperable8) -> list[int]:
    uops = BASE.copy()

    uops[1] |= Ctrl.COUNT_DEC_SP
    uops[2] |= (
        Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | reg.DBUS_ASSERT | Ctrl.CTRL_RST_USEQ
    )
    return uops


def push16(reg: StackOperable16) -> list[int]:
    uops = BASE.copy()

    uops[1] |= Ctrl.COUNT_DEC_SP
    uops[2] |= (
        Ctrl.ADDR_ASSERT_SP
        | Ctrl.DBUS_LOAD_MEM
        | Ctrl.DBUS_ASSERT_LSB
        | reg.XFER_ASSERT
        | Ctrl.COUNT_DEC_SP
    )
    uops[3] |= (
        Ctrl.ADDR_ASSERT_SP
        | Ctrl.DBUS_LOAD_MEM
        | Ctrl.DBUS_ASSERT_MSB
        | reg.XFER_ASSERT
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def pop8(reg: StackOperable8) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_SP
        | Ctrl.DBUS_ASSERT_MEM
        | reg.DBUS_LOAD
        | Ctrl.COUNT_INC_SP
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def pop16(reg: StackOperable16) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_SP
        | Ctrl.DBUS_ASSERT_MEM
        | reg.DBUS_LOAD_HI
        | Ctrl.COUNT_INC_SP
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_SP
        | Ctrl.DBUS_ASSERT_MEM
        | reg.DBUS_LOAD_LO
        | Ctrl.COUNT_INC_SP
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def cmp_gpr_gpr(lhs: GPR, rhs: GPR) -> list[int]:
    uops = BASE.copy()
    XFER_ASSERT = lhs.xfer_assert(rhs)

    uops[1] |= Ctrl.ALU_SEC
    uops[2] |= Ctrl.ALU_SBC | XFER_ASSERT | Ctrl.CTRL_RST_USEQ
    return uops


def cmp_gpr_imm(lhs: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
        | Ctrl.ALU_SEC
    )
    uops[2] |= Ctrl.ALU_SBC | lhs.XFER_ASSERT_TL | Ctrl.CTRL_RST_USEQ
    return uops


def cmp_gpr_dp(lhs: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.ALU_SEC
    )
    uops[3] |= Ctrl.ALU_SBC | lhs.XFER_ASSERT_TL | Ctrl.CTRL_RST_USEQ
    return uops


def cmp_dp_gpr(rhs: GPR) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_DA
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.ALU_SEC
    )
    uops[3] |= Ctrl.ALU_SBC | rhs.XFER_ASSERT_TH | Ctrl.CTRL_RST_USEQ
    return uops


def tst_gpr(reg: GPR) -> list[int]:
    uops = BASE.copy()
    XFER_ASSERT = reg.xfer_assert(reg)

    uops[1] |= Ctrl.ALU_AND | XFER_ASSERT | Ctrl.CTRL_RST_USEQ
    return uops


def jsr_ptr(ptr: GPP) -> list[int]:
    uops = BASE.copy()

    uops[1] |= Ctrl.COUNT_DEC_SP
    uops[2] |= (
        Ctrl.ADDR_ASSERT_SP
        | Ctrl.DBUS_LOAD_MEM
        | Ctrl.DBUS_ASSERT_LSB
        | Ctrl.XFER_ASSERT_PC
        | Ctrl.COUNT_DEC_SP
    )
    uops[3] |= (
        Ctrl.ADDR_ASSERT_SP
        | Ctrl.DBUS_LOAD_MEM
        | Ctrl.DBUS_ASSERT_MSB
        | Ctrl.XFER_ASSERT_PC
    )
    uops[4] |= ptr.XFER_ASSERT | Ctrl.XFER_LOAD_PC | Ctrl.CTRL_RST_USEQ
    return uops


def jmp_abs(pred: Callable[[], bool]) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TH
        | Ctrl.COUNT_INC_PC
    )
    uops[2] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_TL
        | Ctrl.COUNT_INC_PC
    )

    if pred():
        uops[3] |= Ctrl.XFER_ASSERT_T | Ctrl.XFER_LOAD_PC | Ctrl.CTRL_RST_USEQ
    else:
        uops[3] |= Ctrl.CTRL_RST_USEQ

    return uops


def jmp_rel(pred: Callable[[], bool]) -> list[int]:
    uops = BASE.copy()

    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.DBUS_LOAD_OFF
        | Ctrl.COUNT_INC_PC
    )

    if pred():
        uops[2] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.OFFSET_EN
            | Ctrl.XFER_ASSERT_ADDR
            | Ctrl.XFER_LOAD_PC
            | Ctrl.CTRL_RST_USEQ
        )
    else:
        uops[2] |= Ctrl.CTRL_RST_USEQ
    return uops


def jmp_ptr(pred: Callable[[], bool], ptr: GPP) -> list[int]:
    uops = BASE.copy()

    if pred():
        uops[1] |= ptr.XFER_ASSERT | Ctrl.XFER_LOAD_PC | Ctrl.CTRL_RST_USEQ
    else:
        uops[1] |= Ctrl.CTRL_RST_USEQ
    return uops


def musteq_imm(gpr: GPR) -> list[int]:
    uops = BASE.copy()
    uops[1] |= (
        Ctrl.ADDR_ASSERT_PC
        | Ctrl.DBUS_ASSERT_MEM
        | Ctrl.COUNT_INC_PC
        | gpr.XFER_ASSERT_TL
        | Ctrl.DBUS_LOAD_MUSTEQ
        | Ctrl.CTRL_RST_USEQ
    )
    return uops


def get_uops(state: State) -> list[int]:
    flags = state.flags
    OP = state.opcode
    mode = state.mode

    if mode == Mode.STALL:
        return STALL_OPS.copy()

    if mode == Mode.IRQ:
        return IRQ_ACK.copy()

    if mode == Mode.NMI:
        return NMI_ACK.copy()

    uops = BASE.copy()

    # Housekeeping / Flag Management
    if OP == Op.NOP:
        uops[1] |= Ctrl.CTRL_RST_USEQ
    elif OP == Op.EXT:
        uops[1] |= Ctrl.CTRL_SET_EXT | FETCH
    elif OP == Op.CLC:
        uops[1] |= Ctrl.ALU_CLC | Ctrl.CTRL_RST_USEQ
    elif OP == Op.CLI:
        uops[1] |= Ctrl.ALU_CLI | Ctrl.CTRL_RST_USEQ
    elif OP == Op.CLV:
        uops[1] |= Ctrl.ALU_CLV | Ctrl.CTRL_RST_USEQ
    elif OP == Op.SEC:
        uops[1] |= Ctrl.ALU_SEC | Ctrl.CTRL_RST_USEQ
    elif OP == Op.SEI:
        uops[1] |= Ctrl.ALU_SEI | Ctrl.CTRL_RST_USEQ

    elif OP == Op.UBR:
        uops[1] |= Ctrl.CTRL_SET_UBR
        uops[2] |= Ctrl.CTRL_RST_USEQ
    elif OP == Op.KBR:
        uops[1] |= Ctrl.CTRL_CLR_UBR
        uops[2] |= Ctrl.CTRL_RST_USEQ

    # 8-bit Moves
    elif OP == Op.MOV_A_B:
        return mov8(GPR.A, GPR.B)
    elif OP == Op.MOV_A_C:
        return mov8(GPR.A, GPR.C)
    elif OP == Op.MOV_A_D:
        return mov8(GPR.A, GPR.D)
    elif OP == Op.MOV_B_A:
        return mov8(GPR.B, GPR.A)
    elif OP == Op.MOV_B_C:
        return mov8(GPR.B, GPR.C)
    elif OP == Op.MOV_B_D:
        return mov8(GPR.B, GPR.D)
    elif OP == Op.MOV_C_A:
        return mov8(GPR.C, GPR.A)
    elif OP == Op.MOV_C_B:
        return mov8(GPR.C, GPR.B)
    elif OP == Op.MOV_C_D:
        return mov8(GPR.C, GPR.D)
    elif OP == Op.MOV_D_A:
        return mov8(GPR.D, GPR.A)
    elif OP == Op.MOV_D_B:
        return mov8(GPR.D, GPR.B)
    elif OP == Op.MOV_D_C:
        return mov8(GPR.D, GPR.C)

    elif OP == Op.MOV_A_DP:
        uops[1] |= Ctrl.DBUS_ASSERT_DP | Ctrl.DBUS_LOAD_A | Ctrl.CTRL_RST_USEQ
    elif OP == Op.MOV_DP_A:
        uops[1] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_DP | Ctrl.CTRL_RST_USEQ
    elif OP == Op.MOV_BR_A:
        uops[1] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_BR | Ctrl.CTRL_RST_USEQ
    elif OP == Op.MOV_A_BR:
        uops[1] |= Ctrl.DBUS_ASSERT_BR | Ctrl.DBUS_LOAD_A | Ctrl.CTRL_RST_USEQ

    # IO Operations
    elif OP == Op.IN_A:
        return in_gpr(GPR.A)
    elif OP == Op.IN_B:
        return in_gpr(GPR.B)
    elif OP == Op.IN_C:
        return in_gpr(GPR.C)
    elif OP == Op.IN_D:
        return in_gpr(GPR.D)
    elif OP == Op.IN_DP:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_DA
            | Ctrl.COUNT_INC_PC
        )
        uops[2] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_TL
            | Ctrl.COUNT_INC_PC
        )
        uops[3] |= Ctrl.ADDR_ASSERT_IO | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
        uops[4] |= (
            Ctrl.ADDR_ASSERT_DP
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_TH
            | Ctrl.CTRL_RST_USEQ
        )

    elif OP == Op.OUT_A:
        return out_gpr(GPR.A)
    elif OP == Op.OUT_B:
        return out_gpr(GPR.B)
    elif OP == Op.OUT_C:
        return out_gpr(GPR.C)
    elif OP == Op.OUT_D:
        return out_gpr(GPR.D)
    elif OP == Op.OUT_DP:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_PORT
            | Ctrl.COUNT_INC_PC
        )
        uops[2] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_DA
            | Ctrl.COUNT_INC_PC
        )
        uops[3] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
        uops[4] |= (
            Ctrl.ADDR_ASSERT_IO
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_TH
            | Ctrl.CTRL_RST_USEQ
        )
    elif OP == Op.OUT_IMM:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_PORT
            | Ctrl.COUNT_INC_PC
        )
        uops[2] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_TH
            | Ctrl.COUNT_INC_PC
        )
        uops[3] |= (
            Ctrl.ADDR_ASSERT_IO
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_TH
            | Ctrl.CTRL_RST_USEQ
        )

    # A Loads
    elif OP == Op.LOAD_A_IMM:
        return load8_imm(GPR.A)
    elif OP == Op.LOAD_A_ABS:
        return load8_abs(GPR.A)
    elif OP == Op.LOAD_A_DP:
        return load8_dp(GPR.A)
    elif OP == Op.LOAD_A_X_IDX:
        return load8_ptr_idx(GPR.A, PTR.X)
    elif OP == Op.LOAD_A_X_A:
        return load8_ptr_gpr(GPR.A, PTR.X, GPR.A)
    elif OP == Op.LOAD_A_X_B:
        return load8_ptr_gpr(GPR.A, PTR.X, GPR.B)
    elif OP == Op.LOAD_A_X_C:
        return load8_ptr_gpr(GPR.A, PTR.X, GPR.C)
    elif OP == Op.LOAD_A_X_D:
        return load8_ptr_gpr(GPR.A, PTR.X, GPR.D)
    elif OP == Op.LOAD_A_Y_IDX:
        return load8_ptr_idx(GPR.A, PTR.Y)
    elif OP == Op.LOAD_A_Y_A:
        return load8_ptr_gpr(GPR.A, PTR.Y, GPR.A)
    elif OP == Op.LOAD_A_Y_B:
        return load8_ptr_gpr(GPR.A, PTR.Y, GPR.B)
    elif OP == Op.LOAD_A_Y_C:
        return load8_ptr_gpr(GPR.A, PTR.Y, GPR.C)
    elif OP == Op.LOAD_A_Y_D:
        return load8_ptr_gpr(GPR.A, PTR.Y, GPR.D)
    elif OP == Op.LOAD_A_SP_IDX:
        return load8_ptr_idx(GPR.A, PTR.SP)
    elif OP == Op.LOAD_A_SP_A:
        return load8_ptr_gpr(GPR.A, PTR.SP, GPR.A)
    elif OP == Op.LOAD_A_SP_B:
        return load8_ptr_gpr(GPR.A, PTR.SP, GPR.B)
    elif OP == Op.LOAD_A_SP_C:
        return load8_ptr_gpr(GPR.A, PTR.SP, GPR.C)
    elif OP == Op.LOAD_A_SP_D:
        return load8_ptr_gpr(GPR.A, PTR.SP, GPR.D)

    # B Loads
    elif OP == Op.LOAD_B_IMM:
        return load8_imm(GPR.B)
    elif OP == Op.LOAD_B_ABS:
        return load8_abs(GPR.B)
    elif OP == Op.LOAD_B_DP:
        return load8_dp(GPR.B)
    elif OP == Op.LOAD_B_X_IDX:
        return load8_ptr_idx(GPR.B, PTR.X)
    elif OP == Op.LOAD_B_X_A:
        return load8_ptr_gpr(GPR.B, PTR.X, GPR.A)
    elif OP == Op.LOAD_B_X_B:
        return load8_ptr_gpr(GPR.B, PTR.X, GPR.B)
    elif OP == Op.LOAD_B_X_C:
        return load8_ptr_gpr(GPR.B, PTR.X, GPR.C)
    elif OP == Op.LOAD_B_X_D:
        return load8_ptr_gpr(GPR.B, PTR.X, GPR.D)
    elif OP == Op.LOAD_B_Y_IDX:
        return load8_ptr_idx(GPR.B, PTR.Y)
    elif OP == Op.LOAD_B_Y_A:
        return load8_ptr_gpr(GPR.B, PTR.Y, GPR.A)
    elif OP == Op.LOAD_B_Y_B:
        return load8_ptr_gpr(GPR.B, PTR.Y, GPR.B)
    elif OP == Op.LOAD_B_Y_C:
        return load8_ptr_gpr(GPR.B, PTR.Y, GPR.C)
    elif OP == Op.LOAD_B_Y_D:
        return load8_ptr_gpr(GPR.B, PTR.Y, GPR.D)
    elif OP == Op.LOAD_B_SP_IDX:
        return load8_ptr_idx(GPR.B, PTR.SP)
    elif OP == Op.LOAD_B_SP_A:
        return load8_ptr_gpr(GPR.B, PTR.SP, GPR.A)
    elif OP == Op.LOAD_B_SP_B:
        return load8_ptr_gpr(GPR.B, PTR.SP, GPR.B)
    elif OP == Op.LOAD_B_SP_C:
        return load8_ptr_gpr(GPR.B, PTR.SP, GPR.C)
    elif OP == Op.LOAD_B_SP_D:
        return load8_ptr_gpr(GPR.B, PTR.SP, GPR.D)

    # C Loads
    elif OP == Op.LOAD_C_IMM:
        return load8_imm(GPR.C)
    elif OP == Op.LOAD_C_ABS:
        return load8_abs(GPR.C)
    elif OP == Op.LOAD_C_DP:
        return load8_dp(GPR.C)
    elif OP == Op.LOAD_C_X_IDX:
        return load8_ptr_idx(GPR.C, PTR.X)
    elif OP == Op.LOAD_C_X_A:
        return load8_ptr_gpr(GPR.C, PTR.X, GPR.A)
    elif OP == Op.LOAD_C_X_B:
        return load8_ptr_gpr(GPR.C, PTR.X, GPR.B)
    elif OP == Op.LOAD_C_X_C:
        return load8_ptr_gpr(GPR.C, PTR.X, GPR.C)
    elif OP == Op.LOAD_C_X_D:
        return load8_ptr_gpr(GPR.C, PTR.X, GPR.D)
    elif OP == Op.LOAD_C_Y_IDX:
        return load8_ptr_idx(GPR.C, PTR.Y)
    elif OP == Op.LOAD_C_Y_A:
        return load8_ptr_gpr(GPR.C, PTR.Y, GPR.A)
    elif OP == Op.LOAD_C_Y_B:
        return load8_ptr_gpr(GPR.C, PTR.Y, GPR.B)
    elif OP == Op.LOAD_C_Y_C:
        return load8_ptr_gpr(GPR.C, PTR.Y, GPR.C)
    elif OP == Op.LOAD_C_Y_D:
        return load8_ptr_gpr(GPR.C, PTR.Y, GPR.D)
    elif OP == Op.LOAD_C_SP_IDX:
        return load8_ptr_idx(GPR.C, PTR.SP)
    elif OP == Op.LOAD_C_SP_A:
        return load8_ptr_gpr(GPR.C, PTR.SP, GPR.A)
    elif OP == Op.LOAD_C_SP_B:
        return load8_ptr_gpr(GPR.C, PTR.SP, GPR.B)
    elif OP == Op.LOAD_C_SP_C:
        return load8_ptr_gpr(GPR.C, PTR.SP, GPR.C)
    elif OP == Op.LOAD_C_SP_D:
        return load8_ptr_gpr(GPR.C, PTR.SP, GPR.D)

    # D Loads
    elif OP == Op.LOAD_D_IMM:
        return load8_imm(GPR.D)
    elif OP == Op.LOAD_D_ABS:
        return load8_abs(GPR.D)
    elif OP == Op.LOAD_D_DP:
        return load8_dp(GPR.D)
    elif OP == Op.LOAD_D_X_IDX:
        return load8_ptr_idx(GPR.D, PTR.X)
    elif OP == Op.LOAD_D_X_A:
        return load8_ptr_gpr(GPR.D, PTR.X, GPR.A)
    elif OP == Op.LOAD_D_X_B:
        return load8_ptr_gpr(GPR.D, PTR.X, GPR.B)
    elif OP == Op.LOAD_D_X_C:
        return load8_ptr_gpr(GPR.D, PTR.X, GPR.C)
    elif OP == Op.LOAD_D_X_D:
        return load8_ptr_gpr(GPR.D, PTR.X, GPR.D)
    elif OP == Op.LOAD_D_Y_IDX:
        return load8_ptr_idx(GPR.D, PTR.Y)
    elif OP == Op.LOAD_D_Y_A:
        return load8_ptr_gpr(GPR.D, PTR.Y, GPR.A)
    elif OP == Op.LOAD_D_Y_B:
        return load8_ptr_gpr(GPR.D, PTR.Y, GPR.B)
    elif OP == Op.LOAD_D_Y_C:
        return load8_ptr_gpr(GPR.D, PTR.Y, GPR.C)
    elif OP == Op.LOAD_D_Y_D:
        return load8_ptr_gpr(GPR.D, PTR.Y, GPR.D)
    elif OP == Op.LOAD_D_SP_IDX:
        return load8_ptr_idx(GPR.D, PTR.SP)
    elif OP == Op.LOAD_D_SP_A:
        return load8_ptr_gpr(GPR.D, PTR.SP, GPR.A)
    elif OP == Op.LOAD_D_SP_B:
        return load8_ptr_gpr(GPR.D, PTR.SP, GPR.B)
    elif OP == Op.LOAD_D_SP_C:
        return load8_ptr_gpr(GPR.D, PTR.SP, GPR.C)
    elif OP == Op.LOAD_D_SP_D:
        return load8_ptr_gpr(GPR.D, PTR.SP, GPR.D)

    # A Stores
    elif OP == Op.STORE_A_ABS:
        return store8_abs(GPR.A)
    elif OP == Op.STORE_A_DP:
        return store8_dp(GPR.A)
    elif OP == Op.STORE_A_X_IDX:
        return store8_ptr_idx(GPR.A, PTR.X)
    elif OP == Op.STORE_A_X_A:
        return store8_ptr_gpr(GPR.A, PTR.X, GPR.A)
    elif OP == Op.STORE_A_X_B:
        return store8_ptr_gpr(GPR.A, PTR.X, GPR.B)
    elif OP == Op.STORE_A_X_C:
        return store8_ptr_gpr(GPR.A, PTR.X, GPR.C)
    elif OP == Op.STORE_A_X_D:
        return store8_ptr_gpr(GPR.A, PTR.X, GPR.D)
    elif OP == Op.STORE_A_Y_IDX:
        return store8_ptr_idx(GPR.A, PTR.Y)
    elif OP == Op.STORE_A_Y_A:
        return store8_ptr_gpr(GPR.A, PTR.Y, GPR.A)
    elif OP == Op.STORE_A_Y_B:
        return store8_ptr_gpr(GPR.A, PTR.Y, GPR.B)
    elif OP == Op.STORE_A_Y_C:
        return store8_ptr_gpr(GPR.A, PTR.Y, GPR.C)
    elif OP == Op.STORE_A_Y_D:
        return store8_ptr_gpr(GPR.A, PTR.Y, GPR.D)
    elif OP == Op.STORE_A_SP_IDX:
        return store8_ptr_idx(GPR.A, PTR.SP)
    elif OP == Op.STORE_A_SP_A:
        return store8_ptr_gpr(GPR.A, PTR.SP, GPR.A)
    elif OP == Op.STORE_A_SP_B:
        return store8_ptr_gpr(GPR.A, PTR.SP, GPR.B)
    elif OP == Op.STORE_A_SP_C:
        return store8_ptr_gpr(GPR.A, PTR.SP, GPR.C)
    elif OP == Op.STORE_A_SP_D:
        return store8_ptr_gpr(GPR.A, PTR.SP, GPR.D)

    # B Stores
    elif OP == Op.STORE_B_ABS:
        return store8_abs(GPR.B)
    elif OP == Op.STORE_B_DP:
        return store8_dp(GPR.B)
    elif OP == Op.STORE_B_X_IDX:
        return store8_ptr_idx(GPR.B, PTR.X)
    elif OP == Op.STORE_B_X_A:
        return store8_ptr_gpr(GPR.B, PTR.X, GPR.A)
    elif OP == Op.STORE_B_X_B:
        return store8_ptr_gpr(GPR.B, PTR.X, GPR.B)
    elif OP == Op.STORE_B_X_C:
        return store8_ptr_gpr(GPR.B, PTR.X, GPR.C)
    elif OP == Op.STORE_B_X_D:
        return store8_ptr_gpr(GPR.B, PTR.X, GPR.D)
    elif OP == Op.STORE_B_Y_IDX:
        return store8_ptr_idx(GPR.B, PTR.Y)
    elif OP == Op.STORE_B_Y_A:
        return store8_ptr_gpr(GPR.B, PTR.Y, GPR.A)
    elif OP == Op.STORE_B_Y_B:
        return store8_ptr_gpr(GPR.B, PTR.Y, GPR.B)
    elif OP == Op.STORE_B_Y_C:
        return store8_ptr_gpr(GPR.B, PTR.Y, GPR.C)
    elif OP == Op.STORE_B_Y_D:
        return store8_ptr_gpr(GPR.B, PTR.Y, GPR.D)
    elif OP == Op.STORE_B_SP_IDX:
        return store8_ptr_idx(GPR.B, PTR.SP)
    elif OP == Op.STORE_B_SP_A:
        return store8_ptr_gpr(GPR.B, PTR.SP, GPR.A)
    elif OP == Op.STORE_B_SP_B:
        return store8_ptr_gpr(GPR.B, PTR.SP, GPR.B)
    elif OP == Op.STORE_B_SP_C:
        return store8_ptr_gpr(GPR.B, PTR.SP, GPR.C)
    elif OP == Op.STORE_B_SP_D:
        return store8_ptr_gpr(GPR.B, PTR.SP, GPR.D)

    # C Stores
    elif OP == Op.STORE_C_ABS:
        return store8_abs(GPR.C)
    elif OP == Op.STORE_C_DP:
        return store8_dp(GPR.C)
    elif OP == Op.STORE_C_X_IDX:
        return store8_ptr_idx(GPR.C, PTR.X)
    elif OP == Op.STORE_C_X_A:
        return store8_ptr_gpr(GPR.C, PTR.X, GPR.A)
    elif OP == Op.STORE_C_X_B:
        return store8_ptr_gpr(GPR.C, PTR.X, GPR.B)
    elif OP == Op.STORE_C_X_C:
        return store8_ptr_gpr(GPR.C, PTR.X, GPR.C)
    elif OP == Op.STORE_C_X_D:
        return store8_ptr_gpr(GPR.C, PTR.X, GPR.D)
    elif OP == Op.STORE_C_Y_IDX:
        return store8_ptr_idx(GPR.C, PTR.Y)
    elif OP == Op.STORE_C_Y_A:
        return store8_ptr_gpr(GPR.C, PTR.Y, GPR.A)
    elif OP == Op.STORE_C_Y_B:
        return store8_ptr_gpr(GPR.C, PTR.Y, GPR.B)
    elif OP == Op.STORE_C_Y_C:
        return store8_ptr_gpr(GPR.C, PTR.Y, GPR.C)
    elif OP == Op.STORE_C_Y_D:
        return store8_ptr_gpr(GPR.C, PTR.Y, GPR.D)
    elif OP == Op.STORE_C_SP_IDX:
        return store8_ptr_idx(GPR.C, PTR.SP)
    elif OP == Op.STORE_C_SP_A:
        return store8_ptr_gpr(GPR.C, PTR.SP, GPR.A)
    elif OP == Op.STORE_C_SP_B:
        return store8_ptr_gpr(GPR.C, PTR.SP, GPR.B)
    elif OP == Op.STORE_C_SP_C:
        return store8_ptr_gpr(GPR.C, PTR.SP, GPR.C)
    elif OP == Op.STORE_C_SP_D:
        return store8_ptr_gpr(GPR.C, PTR.SP, GPR.D)

    # D Stores
    elif OP == Op.STORE_D_ABS:
        return store8_abs(GPR.D)
    elif OP == Op.STORE_D_DP:
        return store8_dp(GPR.D)
    elif OP == Op.STORE_D_X_IDX:
        return store8_ptr_idx(GPR.D, PTR.X)
    elif OP == Op.STORE_D_X_A:
        return store8_ptr_gpr(GPR.D, PTR.X, GPR.A)
    elif OP == Op.STORE_D_X_B:
        return store8_ptr_gpr(GPR.D, PTR.X, GPR.B)
    elif OP == Op.STORE_D_X_C:
        return store8_ptr_gpr(GPR.D, PTR.X, GPR.C)
    elif OP == Op.STORE_D_X_D:
        return store8_ptr_gpr(GPR.D, PTR.X, GPR.D)
    elif OP == Op.STORE_D_Y_IDX:
        return store8_ptr_idx(GPR.D, PTR.Y)
    elif OP == Op.STORE_D_Y_A:
        return store8_ptr_gpr(GPR.D, PTR.Y, GPR.A)
    elif OP == Op.STORE_D_Y_B:
        return store8_ptr_gpr(GPR.D, PTR.Y, GPR.B)
    elif OP == Op.STORE_D_Y_C:
        return store8_ptr_gpr(GPR.D, PTR.Y, GPR.C)
    elif OP == Op.STORE_D_Y_D:
        return store8_ptr_gpr(GPR.D, PTR.Y, GPR.D)
    elif OP == Op.STORE_D_SP_IDX:
        return store8_ptr_idx(GPR.D, PTR.SP)
    elif OP == Op.STORE_D_SP_A:
        return store8_ptr_gpr(GPR.D, PTR.SP, GPR.A)
    elif OP == Op.STORE_D_SP_B:
        return store8_ptr_gpr(GPR.D, PTR.SP, GPR.B)
    elif OP == Op.STORE_D_SP_C:
        return store8_ptr_gpr(GPR.D, PTR.SP, GPR.C)
    elif OP == Op.STORE_D_SP_D:
        return store8_ptr_gpr(GPR.D, PTR.SP, GPR.D)

    # 16-bit Moves
    elif OP == Op.MOV_X_Y:
        return mov16(MOV16.X, MOV16.Y)
    elif OP == Op.MOV_X_AB:
        uops[1] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_XH
        uops[2] |= Ctrl.DBUS_ASSERT_B | Ctrl.DBUS_LOAD_XL | Ctrl.CTRL_RST_USEQ
    elif OP == Op.MOV_X_CD:
        uops[1] |= Ctrl.DBUS_ASSERT_C | Ctrl.DBUS_LOAD_XH
        uops[2] |= Ctrl.DBUS_ASSERT_D | Ctrl.DBUS_LOAD_XL | Ctrl.CTRL_RST_USEQ

    elif OP == Op.MOV_Y_X:
        return mov16(MOV16.Y, MOV16.X)
    elif OP == Op.MOV_Y_AB:
        uops[1] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_YH
        uops[2] |= Ctrl.DBUS_ASSERT_B | Ctrl.DBUS_LOAD_YL | Ctrl.CTRL_RST_USEQ
    elif OP == Op.MOV_Y_CD:
        uops[1] |= Ctrl.DBUS_ASSERT_C | Ctrl.DBUS_LOAD_YH
        uops[2] |= Ctrl.DBUS_ASSERT_D | Ctrl.DBUS_LOAD_YL | Ctrl.CTRL_RST_USEQ

    elif OP == Op.MOV_AB_X:
        uops[1] |= Ctrl.XFER_ASSERT_X | Ctrl.DBUS_ASSERT_MSB | Ctrl.DBUS_LOAD_A
        uops[2] |= Ctrl.XFER_ASSERT_X | Ctrl.DBUS_ASSERT_LSB | Ctrl.DBUS_LOAD_B
    elif OP == Op.MOV_AB_Y:
        uops[1] |= Ctrl.XFER_ASSERT_Y | Ctrl.DBUS_ASSERT_MSB | Ctrl.DBUS_LOAD_A
        uops[2] |= Ctrl.XFER_ASSERT_Y | Ctrl.DBUS_ASSERT_LSB | Ctrl.DBUS_LOAD_B

    elif OP == Op.MOV_CD_X:
        uops[1] |= Ctrl.XFER_ASSERT_X | Ctrl.DBUS_ASSERT_MSB | Ctrl.DBUS_LOAD_C
        uops[2] |= Ctrl.XFER_ASSERT_X | Ctrl.DBUS_ASSERT_LSB | Ctrl.DBUS_LOAD_D
    elif OP == Op.MOV_CD_Y:
        uops[1] |= Ctrl.XFER_ASSERT_Y | Ctrl.DBUS_ASSERT_MSB | Ctrl.DBUS_LOAD_C
        uops[2] |= Ctrl.XFER_ASSERT_Y | Ctrl.DBUS_ASSERT_LSB | Ctrl.DBUS_LOAD_D

    elif OP == Op.MOV_SP_X:
        uops[1] |= Ctrl.XFER_ASSERT_X | Ctrl.XFER_LOAD_SP | Ctrl.CTRL_RST_USEQ
    elif OP == Op.MOV_X_SP:
        uops[1] |= Ctrl.XFER_ASSERT_SP | Ctrl.XFER_LOAD_X | Ctrl.CTRL_RST_USEQ

    # X Loads
    elif OP == Op.LOAD_X_IMM:
        return load16_imm(GPP.X)
    elif OP == Op.LOAD_X_ABS:
        return load16_abs(GPP.X)
    elif OP == Op.LOAD_X_DP:
        return load16_dp(GPP.X)
    elif OP == Op.LOAD_X_X_IDX:
        return load16_ptr_idx(GPP.X, PTR.X)
    elif OP == Op.LOAD_X_Y_IDX:
        return load16_ptr_idx(GPP.X, PTR.Y)
    elif OP == Op.LOAD_X_SP_IDX:
        return load16_ptr_idx(GPP.X, PTR.SP)

    # Y Loads
    elif OP == Op.LOAD_Y_IMM:
        return load16_imm(GPP.Y)
    elif OP == Op.LOAD_Y_ABS:
        return load16_abs(GPP.Y)
    elif OP == Op.LOAD_Y_DP:
        return load16_dp(GPP.Y)
    elif OP == Op.LOAD_Y_X_IDX:
        return load16_ptr_idx(GPP.Y, PTR.X)
    elif OP == Op.LOAD_Y_Y_IDX:
        return load16_ptr_idx(GPP.Y, PTR.Y)
    elif OP == Op.LOAD_Y_SP_IDX:
        return load16_ptr_idx(GPP.Y, PTR.SP)

    # X Stores
    elif OP == Op.STORE_X_ABS:
        return store16_abs(GPP.X)
    elif OP == Op.STORE_X_DP:
        return store16_dp(GPP.X)
    elif OP == Op.STORE_X_X_IDX:
        return store16_ptr_idx(GPP.X, PTR.X)
    elif OP == Op.STORE_X_Y_IDX:
        return store16_ptr_idx(GPP.X, PTR.Y)
    elif OP == Op.STORE_X_SP_IDX:
        return store16_ptr_idx(GPP.X, PTR.SP)

    # Y Stores
    elif OP == Op.STORE_Y_ABS:
        return store16_abs(GPP.Y)
    elif OP == Op.STORE_Y_DP:
        return store16_dp(GPP.Y)
    elif OP == Op.STORE_Y_X_IDX:
        return store16_ptr_idx(GPP.Y, PTR.X)
    elif OP == Op.STORE_Y_Y_IDX:
        return store16_ptr_idx(GPP.Y, PTR.Y)
    elif OP == Op.STORE_Y_SP_IDX:
        return store16_ptr_idx(GPP.Y, PTR.SP)

    # Load Effective Address
    elif OP == Op.LEA_X_A:
        return lea_gpr(PTR.X, GPR.A)
    elif OP == Op.LEA_X_B:
        return lea_gpr(PTR.X, GPR.B)
    elif OP == Op.LEA_X_C:
        return lea_gpr(PTR.X, GPR.C)
    elif OP == Op.LEA_X_D:
        return lea_gpr(PTR.X, GPR.D)
    elif OP == Op.LEA_X_IDX:
        return lea_idx(PTR.X)

    elif OP == Op.LEA_Y_A:
        return lea_gpr(PTR.Y, GPR.A)
    elif OP == Op.LEA_Y_B:
        return lea_gpr(PTR.Y, GPR.B)
    elif OP == Op.LEA_Y_C:
        return lea_gpr(PTR.Y, GPR.C)
    elif OP == Op.LEA_Y_D:
        return lea_gpr(PTR.Y, GPR.D)
    elif OP == Op.LEA_Y_IDX:
        return lea_idx(PTR.Y)

    elif OP == Op.LEA_SP_A:
        return lea_gpr(PTR.SP, GPR.A)
    elif OP == Op.LEA_SP_B:
        return lea_gpr(PTR.SP, GPR.B)
    elif OP == Op.LEA_SP_C:
        return lea_gpr(PTR.SP, GPR.C)
    elif OP == Op.LEA_SP_D:
        return lea_gpr(PTR.SP, GPR.D)
    elif OP == Op.LEA_SP_IDX:
        return lea_idx(PTR.SP)

    # Add with Carry
    elif OP == Op.ADC_A_A:
        return binop_gpr_gpr(BinOp.ADC, GPR.A, GPR.A)
    elif OP == Op.ADC_A_B:
        return binop_gpr_gpr(BinOp.ADC, GPR.A, GPR.B)
    elif OP == Op.ADC_A_C:
        return binop_gpr_gpr(BinOp.ADC, GPR.A, GPR.C)
    elif OP == Op.ADC_A_D:
        return binop_gpr_gpr(BinOp.ADC, GPR.A, GPR.D)
    elif OP == Op.ADC_A_IMM:
        return binop_gpr_imm(BinOp.ADC, GPR.A)
    elif OP == Op.ADC_A_DP:
        return binop_gpr_dp(BinOp.ADC, GPR.A)

    elif OP == Op.ADC_B_A:
        return binop_gpr_gpr(BinOp.ADC, GPR.B, GPR.A)
    elif OP == Op.ADC_B_B:
        return binop_gpr_gpr(BinOp.ADC, GPR.B, GPR.B)
    elif OP == Op.ADC_B_C:
        return binop_gpr_gpr(BinOp.ADC, GPR.B, GPR.C)
    elif OP == Op.ADC_B_D:
        return binop_gpr_gpr(BinOp.ADC, GPR.B, GPR.D)
    elif OP == Op.ADC_B_IMM:
        return binop_gpr_imm(BinOp.ADC, GPR.B)
    elif OP == Op.ADC_B_DP:
        return binop_gpr_dp(BinOp.ADC, GPR.B)

    elif OP == Op.ADC_C_A:
        return binop_gpr_gpr(BinOp.ADC, GPR.C, GPR.A)
    elif OP == Op.ADC_C_B:
        return binop_gpr_gpr(BinOp.ADC, GPR.C, GPR.B)
    elif OP == Op.ADC_C_C:
        return binop_gpr_gpr(BinOp.ADC, GPR.C, GPR.C)
    elif OP == Op.ADC_C_D:
        return binop_gpr_gpr(BinOp.ADC, GPR.C, GPR.D)
    elif OP == Op.ADC_C_IMM:
        return binop_gpr_imm(BinOp.ADC, GPR.C)
    elif OP == Op.ADC_C_DP:
        return binop_gpr_dp(BinOp.ADC, GPR.C)

    elif OP == Op.ADC_D_A:
        return binop_gpr_gpr(BinOp.ADC, GPR.D, GPR.A)
    elif OP == Op.ADC_D_B:
        return binop_gpr_gpr(BinOp.ADC, GPR.D, GPR.B)
    elif OP == Op.ADC_D_C:
        return binop_gpr_gpr(BinOp.ADC, GPR.D, GPR.C)
    elif OP == Op.ADC_D_D:
        return binop_gpr_gpr(BinOp.ADC, GPR.D, GPR.D)
    elif OP == Op.ADC_D_IMM:
        return binop_gpr_imm(BinOp.ADC, GPR.D)
    elif OP == Op.ADC_D_DP:
        return binop_gpr_dp(BinOp.ADC, GPR.D)

    elif OP == Op.ADC_DP_A:
        return binop_dp_gpr(BinOp.ADC, GPR.A)
    elif OP == Op.ADC_DP_B:
        return binop_dp_gpr(BinOp.ADC, GPR.B)
    elif OP == Op.ADC_DP_C:
        return binop_dp_gpr(BinOp.ADC, GPR.C)
    elif OP == Op.ADC_DP_D:
        return binop_dp_gpr(BinOp.ADC, GPR.D)
    elif OP == Op.ADC_DP_IMM:
        return binop_dp_imm(BinOp.ADC)

    # Subtract with Carry
    elif OP == Op.SBC_A_A:
        return binop_gpr_gpr(BinOp.SBC, GPR.A, GPR.A)
    elif OP == Op.SBC_A_B:
        return binop_gpr_gpr(BinOp.SBC, GPR.A, GPR.B)
    elif OP == Op.SBC_A_C:
        return binop_gpr_gpr(BinOp.SBC, GPR.A, GPR.C)
    elif OP == Op.SBC_A_D:
        return binop_gpr_gpr(BinOp.SBC, GPR.A, GPR.D)
    elif OP == Op.SBC_A_IMM:
        return binop_gpr_imm(BinOp.SBC, GPR.A)
    elif OP == Op.SBC_A_DP:
        return binop_gpr_dp(BinOp.SBC, GPR.A)

    elif OP == Op.SBC_B_A:
        return binop_gpr_gpr(BinOp.SBC, GPR.B, GPR.A)
    elif OP == Op.SBC_B_B:
        return binop_gpr_gpr(BinOp.SBC, GPR.B, GPR.B)
    elif OP == Op.SBC_B_C:
        return binop_gpr_gpr(BinOp.SBC, GPR.B, GPR.C)
    elif OP == Op.SBC_B_D:
        return binop_gpr_gpr(BinOp.SBC, GPR.B, GPR.D)
    elif OP == Op.SBC_B_IMM:
        return binop_gpr_imm(BinOp.SBC, GPR.B)
    elif OP == Op.SBC_B_DP:
        return binop_gpr_dp(BinOp.SBC, GPR.B)

    elif OP == Op.SBC_C_A:
        return binop_gpr_gpr(BinOp.SBC, GPR.C, GPR.A)
    elif OP == Op.SBC_C_B:
        return binop_gpr_gpr(BinOp.SBC, GPR.C, GPR.B)
    elif OP == Op.SBC_C_C:
        return binop_gpr_gpr(BinOp.SBC, GPR.C, GPR.C)
    elif OP == Op.SBC_C_D:
        return binop_gpr_gpr(BinOp.SBC, GPR.C, GPR.D)
    elif OP == Op.SBC_C_IMM:
        return binop_gpr_imm(BinOp.SBC, GPR.C)
    elif OP == Op.SBC_C_DP:
        return binop_gpr_dp(BinOp.SBC, GPR.C)

    elif OP == Op.SBC_D_A:
        return binop_gpr_gpr(BinOp.SBC, GPR.D, GPR.A)
    elif OP == Op.SBC_D_B:
        return binop_gpr_gpr(BinOp.SBC, GPR.D, GPR.B)
    elif OP == Op.SBC_D_C:
        return binop_gpr_gpr(BinOp.SBC, GPR.D, GPR.C)
    elif OP == Op.SBC_D_D:
        return binop_gpr_gpr(BinOp.SBC, GPR.D, GPR.D)
    elif OP == Op.SBC_D_IMM:
        return binop_gpr_imm(BinOp.SBC, GPR.D)
    elif OP == Op.SBC_D_DP:
        return binop_gpr_dp(BinOp.SBC, GPR.D)

    elif OP == Op.SBC_DP_A:
        return binop_dp_gpr(BinOp.SBC, GPR.A)
    elif OP == Op.SBC_DP_B:
        return binop_dp_gpr(BinOp.SBC, GPR.B)
    elif OP == Op.SBC_DP_C:
        return binop_dp_gpr(BinOp.SBC, GPR.C)
    elif OP == Op.SBC_DP_D:
        return binop_dp_gpr(BinOp.SBC, GPR.D)
    elif OP == Op.SBC_DP_IMM:
        return binop_dp_imm(BinOp.SBC)

    # Logical AND
    elif OP == Op.AND_A_B:
        return binop_gpr_gpr(BinOp.AND, GPR.A, GPR.B)
    elif OP == Op.AND_A_C:
        return binop_gpr_gpr(BinOp.AND, GPR.A, GPR.C)
    elif OP == Op.AND_A_D:
        return binop_gpr_gpr(BinOp.AND, GPR.A, GPR.D)
    elif OP == Op.AND_A_IMM:
        return binop_gpr_imm(BinOp.AND, GPR.A)
    elif OP == Op.AND_A_DP:
        return binop_gpr_dp(BinOp.AND, GPR.A)

    elif OP == Op.AND_B_A:
        return binop_gpr_gpr(BinOp.AND, GPR.B, GPR.A)
    elif OP == Op.AND_B_C:
        return binop_gpr_gpr(BinOp.AND, GPR.B, GPR.C)
    elif OP == Op.AND_B_D:
        return binop_gpr_gpr(BinOp.AND, GPR.B, GPR.D)
    elif OP == Op.AND_B_IMM:
        return binop_gpr_imm(BinOp.AND, GPR.B)
    elif OP == Op.AND_B_DP:
        return binop_gpr_dp(BinOp.AND, GPR.B)

    elif OP == Op.AND_C_A:
        return binop_gpr_gpr(BinOp.AND, GPR.C, GPR.A)
    elif OP == Op.AND_C_B:
        return binop_gpr_gpr(BinOp.AND, GPR.C, GPR.B)
    elif OP == Op.AND_C_D:
        return binop_gpr_gpr(BinOp.AND, GPR.C, GPR.D)
    elif OP == Op.AND_C_IMM:
        return binop_gpr_imm(BinOp.AND, GPR.C)
    elif OP == Op.AND_C_DP:
        return binop_gpr_dp(BinOp.AND, GPR.C)

    elif OP == Op.AND_D_A:
        return binop_gpr_gpr(BinOp.AND, GPR.D, GPR.A)
    elif OP == Op.AND_D_B:
        return binop_gpr_gpr(BinOp.AND, GPR.D, GPR.B)
    elif OP == Op.AND_D_C:
        return binop_gpr_gpr(BinOp.AND, GPR.D, GPR.C)
    elif OP == Op.AND_D_IMM:
        return binop_gpr_imm(BinOp.AND, GPR.D)
    elif OP == Op.AND_D_DP:
        return binop_gpr_dp(BinOp.AND, GPR.D)

    elif OP == Op.AND_DP_A:
        return binop_dp_gpr(BinOp.AND, GPR.A)
    elif OP == Op.AND_DP_B:
        return binop_dp_gpr(BinOp.AND, GPR.B)
    elif OP == Op.AND_DP_C:
        return binop_dp_gpr(BinOp.AND, GPR.C)
    elif OP == Op.AND_DP_D:
        return binop_dp_gpr(BinOp.AND, GPR.D)
    elif OP == Op.AND_DP_IMM:
        return binop_dp_imm(BinOp.AND)

    # Logical OR
    elif OP == Op.OR_A_B:
        return binop_gpr_gpr(BinOp.OR, GPR.A, GPR.B)
    elif OP == Op.OR_A_C:
        return binop_gpr_gpr(BinOp.OR, GPR.A, GPR.C)
    elif OP == Op.OR_A_D:
        return binop_gpr_gpr(BinOp.OR, GPR.A, GPR.D)
    elif OP == Op.OR_A_IMM:
        return binop_gpr_imm(BinOp.OR, GPR.A)
    elif OP == Op.OR_A_DP:
        return binop_gpr_dp(BinOp.OR, GPR.A)

    elif OP == Op.OR_B_A:
        return binop_gpr_gpr(BinOp.OR, GPR.B, GPR.A)
    elif OP == Op.OR_B_C:
        return binop_gpr_gpr(BinOp.OR, GPR.B, GPR.C)
    elif OP == Op.OR_B_D:
        return binop_gpr_gpr(BinOp.OR, GPR.B, GPR.D)
    elif OP == Op.OR_B_IMM:
        return binop_gpr_imm(BinOp.OR, GPR.B)
    elif OP == Op.OR_B_DP:
        return binop_gpr_dp(BinOp.OR, GPR.B)

    elif OP == Op.OR_C_A:
        return binop_gpr_gpr(BinOp.OR, GPR.C, GPR.A)
    elif OP == Op.OR_C_B:
        return binop_gpr_gpr(BinOp.OR, GPR.C, GPR.B)
    elif OP == Op.OR_C_D:
        return binop_gpr_gpr(BinOp.OR, GPR.C, GPR.D)
    elif OP == Op.OR_C_IMM:
        return binop_gpr_imm(BinOp.OR, GPR.C)
    elif OP == Op.OR_C_DP:
        return binop_gpr_dp(BinOp.OR, GPR.C)

    elif OP == Op.OR_D_A:
        return binop_gpr_gpr(BinOp.OR, GPR.D, GPR.A)
    elif OP == Op.OR_D_B:
        return binop_gpr_gpr(BinOp.OR, GPR.D, GPR.B)
    elif OP == Op.OR_D_C:
        return binop_gpr_gpr(BinOp.OR, GPR.D, GPR.C)
    elif OP == Op.OR_D_IMM:
        return binop_gpr_imm(BinOp.OR, GPR.D)
    elif OP == Op.OR_D_DP:
        return binop_gpr_dp(BinOp.OR, GPR.D)

    elif OP == Op.OR_DP_A:
        return binop_dp_gpr(BinOp.OR, GPR.A)
    elif OP == Op.OR_DP_B:
        return binop_dp_gpr(BinOp.OR, GPR.B)
    elif OP == Op.OR_DP_C:
        return binop_dp_gpr(BinOp.OR, GPR.C)
    elif OP == Op.OR_DP_D:
        return binop_dp_gpr(BinOp.OR, GPR.D)
    elif OP == Op.OR_DP_IMM:
        return binop_dp_imm(BinOp.OR)

    # Logical XOR
    elif OP == Op.XOR_A_A:
        return binop_gpr_gpr(BinOp.XOR, GPR.A, GPR.A)
    elif OP == Op.XOR_A_B:
        return binop_gpr_gpr(BinOp.XOR, GPR.A, GPR.B)
    elif OP == Op.XOR_A_C:
        return binop_gpr_gpr(BinOp.XOR, GPR.A, GPR.C)
    elif OP == Op.XOR_A_D:
        return binop_gpr_gpr(BinOp.XOR, GPR.A, GPR.D)
    elif OP == Op.XOR_A_IMM:
        return binop_gpr_imm(BinOp.XOR, GPR.A)
    elif OP == Op.XOR_A_DP:
        return binop_gpr_dp(BinOp.XOR, GPR.A)

    elif OP == Op.XOR_B_A:
        return binop_gpr_gpr(BinOp.XOR, GPR.B, GPR.A)
    elif OP == Op.XOR_B_B:
        return binop_gpr_gpr(BinOp.XOR, GPR.B, GPR.B)
    elif OP == Op.XOR_B_C:
        return binop_gpr_gpr(BinOp.XOR, GPR.B, GPR.C)
    elif OP == Op.XOR_B_D:
        return binop_gpr_gpr(BinOp.XOR, GPR.B, GPR.D)
    elif OP == Op.XOR_B_IMM:
        return binop_gpr_imm(BinOp.XOR, GPR.B)
    elif OP == Op.XOR_B_DP:
        return binop_gpr_dp(BinOp.XOR, GPR.B)

    elif OP == Op.XOR_C_A:
        return binop_gpr_gpr(BinOp.XOR, GPR.C, GPR.A)
    elif OP == Op.XOR_C_B:
        return binop_gpr_gpr(BinOp.XOR, GPR.C, GPR.B)
    elif OP == Op.XOR_C_C:
        return binop_gpr_gpr(BinOp.XOR, GPR.C, GPR.C)
    elif OP == Op.XOR_C_D:
        return binop_gpr_gpr(BinOp.XOR, GPR.C, GPR.D)
    elif OP == Op.XOR_C_IMM:
        return binop_gpr_imm(BinOp.XOR, GPR.C)
    elif OP == Op.XOR_C_DP:
        return binop_gpr_dp(BinOp.XOR, GPR.C)

    elif OP == Op.XOR_D_A:
        return binop_gpr_gpr(BinOp.XOR, GPR.D, GPR.A)
    elif OP == Op.XOR_D_B:
        return binop_gpr_gpr(BinOp.XOR, GPR.D, GPR.B)
    elif OP == Op.XOR_D_C:
        return binop_gpr_gpr(BinOp.XOR, GPR.D, GPR.C)
    elif OP == Op.XOR_D_D:
        return binop_gpr_gpr(BinOp.XOR, GPR.D, GPR.D)
    elif OP == Op.XOR_D_IMM:
        return binop_gpr_imm(BinOp.XOR, GPR.D)
    elif OP == Op.XOR_D_DP:
        return binop_gpr_dp(BinOp.XOR, GPR.D)

    elif OP == Op.XOR_DP_A:
        return binop_dp_gpr(BinOp.XOR, GPR.A)
    elif OP == Op.XOR_DP_B:
        return binop_dp_gpr(BinOp.XOR, GPR.B)
    elif OP == Op.XOR_DP_C:
        return binop_dp_gpr(BinOp.XOR, GPR.C)
    elif OP == Op.XOR_DP_D:
        return binop_dp_gpr(BinOp.XOR, GPR.D)
    elif OP == Op.XOR_DP_IMM:
        return binop_dp_imm(BinOp.XOR)

    # Logical NOT
    elif OP == Op.NOT_A:
        return unyop_gpr(UnyOp.NOT, GPR.A)
    elif OP == Op.NOT_B:
        return unyop_gpr(UnyOp.NOT, GPR.B)
    elif OP == Op.NOT_C:
        return unyop_gpr(UnyOp.NOT, GPR.C)
    elif OP == Op.NOT_D:
        return unyop_gpr(UnyOp.NOT, GPR.D)
    elif OP == Op.NOT_DP:
        return unyop_dp(UnyOp.NOT)

    # Negation (2s Complement)
    elif OP == Op.NEG_A:
        return neg_gpr(GPR.A)
    elif OP == Op.NEG_B:
        return neg_gpr(GPR.B)
    elif OP == Op.NEG_C:
        return neg_gpr(GPR.C)
    elif OP == Op.NEG_D:
        return neg_gpr(GPR.D)
    elif OP == Op.NEG_DP:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_DA
            | Ctrl.COUNT_INC_PC
        )
        uops[2] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL
        uops[3] |= (
            Ctrl.ALU_NOT | Ctrl.XFER_ASSERT_T | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TL
        )
        uops[4] |= (
            Ctrl.ALU_INC | Ctrl.XFER_ASSERT_T | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TL
        )
        uops[5] |= (
            Ctrl.ADDR_ASSERT_DP
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_TL
            | Ctrl.CTRL_RST_USEQ
        )

    # Shift Right with Carry
    elif OP == Op.SRC_A:
        return unyop_gpr(UnyOp.SRC, GPR.A)
    elif OP == Op.SRC_B:
        return unyop_gpr(UnyOp.SRC, GPR.B)
    elif OP == Op.SRC_C:
        return unyop_gpr(UnyOp.SRC, GPR.C)
    elif OP == Op.SRC_D:
        return unyop_gpr(UnyOp.SRC, GPR.D)
    elif OP == Op.SRC_DP:
        return unyop_dp(UnyOp.SRC)

    # Arithmetic Shift Right
    elif OP == Op.ASR_A:
        return unyop_gpr(UnyOp.ASR, GPR.A)
    elif OP == Op.ASR_B:
        return unyop_gpr(UnyOp.ASR, GPR.B)
    elif OP == Op.ASR_C:
        return unyop_gpr(UnyOp.ASR, GPR.C)
    elif OP == Op.ASR_D:
        return unyop_gpr(UnyOp.ASR, GPR.D)
    elif OP == Op.ASR_DP:
        return unyop_dp(UnyOp.ASR)

    # Increment
    elif OP == Op.INC_A:
        return unyop_gpr(UnyOp.INC, GPR.A)
    elif OP == Op.INC_B:
        return unyop_gpr(UnyOp.INC, GPR.B)
    elif OP == Op.INC_C:
        return unyop_gpr(UnyOp.INC, GPR.C)
    elif OP == Op.INC_D:
        return unyop_gpr(UnyOp.INC, GPR.D)
    elif OP == Op.INC_DP:
        return unyop_dp(UnyOp.INC)

    elif OP == Op.INC_X:
        uops[1] |= Ctrl.COUNT_INC_X | Ctrl.CTRL_RST_USEQ
    elif OP == Op.INC_Y:
        uops[1] |= Ctrl.COUNT_INC_Y | Ctrl.CTRL_RST_USEQ

    # Decrement
    elif OP == Op.DEC_A:
        return unyop_gpr(UnyOp.DEC, GPR.A)
    elif OP == Op.DEC_B:
        return unyop_gpr(UnyOp.DEC, GPR.B)
    elif OP == Op.DEC_C:
        return unyop_gpr(UnyOp.DEC, GPR.C)
    elif OP == Op.DEC_D:
        return unyop_gpr(UnyOp.DEC, GPR.D)
    elif OP == Op.DEC_DP:
        return unyop_dp(UnyOp.DEC)

    elif OP == Op.DEC_X:
        uops[1] |= Ctrl.COUNT_DEC_X | Ctrl.CTRL_RST_USEQ
    elif OP == Op.DEC_Y:
        uops[1] |= Ctrl.COUNT_DEC_Y | Ctrl.CTRL_RST_USEQ

    # Stack Pushes
    elif OP == Op.PUSH_A:
        return push8(StackOperable8.A)
    elif OP == Op.PUSH_B:
        return push8(StackOperable8.B)
    elif OP == Op.PUSH_C:
        return push8(StackOperable8.C)
    elif OP == Op.PUSH_D:
        return push8(StackOperable8.D)
    elif OP == Op.PUSH_X:
        return push16(StackOperable16.X)
    elif OP == Op.PUSH_Y:
        return push16(StackOperable16.Y)

    # Stack Pops
    elif OP == Op.POP_A:
        return pop8(StackOperable8.A)
    elif OP == Op.POP_B:
        return pop8(StackOperable8.B)
    elif OP == Op.POP_C:
        return pop8(StackOperable8.C)
    elif OP == Op.POP_D:
        return pop8(StackOperable8.D)
    elif OP == Op.POP_X:
        return pop16(StackOperable16.X)
    elif OP == Op.POP_Y:
        return pop16(StackOperable16.Y)

    # Compares
    elif OP == Op.CMP_A_A:
        return cmp_gpr_gpr(GPR.A, GPR.A)
    elif OP == Op.CMP_A_B:
        return cmp_gpr_gpr(GPR.A, GPR.B)
    elif OP == Op.CMP_A_C:
        return cmp_gpr_gpr(GPR.A, GPR.C)
    elif OP == Op.CMP_A_D:
        return cmp_gpr_gpr(GPR.A, GPR.D)
    elif OP == Op.CMP_A_IMM:
        return cmp_gpr_imm(GPR.A)
    elif OP == Op.CMP_A_DP:
        return cmp_gpr_dp(GPR.A)

    elif OP == Op.CMP_B_A:
        return cmp_gpr_gpr(GPR.B, GPR.A)
    elif OP == Op.CMP_B_B:
        return cmp_gpr_gpr(GPR.B, GPR.B)
    elif OP == Op.CMP_B_C:
        return cmp_gpr_gpr(GPR.B, GPR.C)
    elif OP == Op.CMP_B_D:
        return cmp_gpr_gpr(GPR.B, GPR.D)
    elif OP == Op.CMP_B_IMM:
        return cmp_gpr_imm(GPR.B)
    elif OP == Op.CMP_B_DP:
        return cmp_gpr_dp(GPR.B)

    elif OP == Op.CMP_C_A:
        return cmp_gpr_gpr(GPR.C, GPR.A)
    elif OP == Op.CMP_C_B:
        return cmp_gpr_gpr(GPR.C, GPR.B)
    elif OP == Op.CMP_C_C:
        return cmp_gpr_gpr(GPR.C, GPR.C)
    elif OP == Op.CMP_C_D:
        return cmp_gpr_gpr(GPR.C, GPR.D)
    elif OP == Op.CMP_C_IMM:
        return cmp_gpr_imm(GPR.C)
    elif OP == Op.CMP_C_DP:
        return cmp_gpr_dp(GPR.C)

    elif OP == Op.CMP_D_A:
        return cmp_gpr_gpr(GPR.D, GPR.A)
    elif OP == Op.CMP_D_B:
        return cmp_gpr_gpr(GPR.D, GPR.B)
    elif OP == Op.CMP_D_C:
        return cmp_gpr_gpr(GPR.D, GPR.C)
    elif OP == Op.CMP_D_D:
        return cmp_gpr_gpr(GPR.D, GPR.D)
    elif OP == Op.CMP_D_IMM:
        return cmp_gpr_imm(GPR.D)
    elif OP == Op.CMP_D_DP:
        return cmp_gpr_dp(GPR.D)

    elif OP == Op.CMP_DP_A:
        return cmp_dp_gpr(GPR.A)
    elif OP == Op.CMP_DP_B:
        return cmp_dp_gpr(GPR.B)
    elif OP == Op.CMP_DP_C:
        return cmp_dp_gpr(GPR.C)
    elif OP == Op.CMP_DP_D:
        return cmp_dp_gpr(GPR.D)
    elif OP == Op.CMP_DP_IMM:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_DA
            | Ctrl.COUNT_INC_PC
        )
        uops[2] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_TL
            | Ctrl.COUNT_INC_PC
        )
        uops[3] |= (
            Ctrl.ADDR_ASSERT_DP
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_TH
            | Ctrl.ALU_SEC
        )
        uops[4] |= Ctrl.ALU_SBC | Ctrl.XFER_ASSERT_T | Ctrl.CTRL_RST_USEQ

    # Tests (Self AND)
    elif OP == Op.TST_A:
        return tst_gpr(GPR.A)
    elif OP == Op.TST_B:
        return tst_gpr(GPR.B)
    elif OP == Op.TST_C:
        return tst_gpr(GPR.C)
    elif OP == Op.TST_D:
        return tst_gpr(GPR.D)
    elif OP == Op.TST_DP:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_DA
            | Ctrl.COUNT_INC_PC
        )
        uops[2] |= Ctrl.ADDR_ASSERT_DP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
        uops[3] |= Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_TL
        uops[4] |= Ctrl.ALU_AND | Ctrl.XFER_ASSERT_T | Ctrl.CTRL_RST_USEQ

    # Subroutine Control
    elif OP == Op.JSR_ABS:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_TH
            | Ctrl.COUNT_INC_PC
        )
        uops[2] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_TL
            | Ctrl.COUNT_INC_PC
            | Ctrl.COUNT_DEC_SP
        )
        uops[3] |= (
            Ctrl.ADDR_ASSERT_SP
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_LSB
            | Ctrl.XFER_ASSERT_PC
            | Ctrl.COUNT_DEC_SP
        )
        uops[4] |= (
            Ctrl.ADDR_ASSERT_SP
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_MSB
            | Ctrl.XFER_ASSERT_PC
        )
        uops[5] |= Ctrl.XFER_ASSERT_T | Ctrl.XFER_LOAD_PC | Ctrl.CTRL_RST_USEQ
    elif OP == Op.JSR_REL:
        uops[1] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_OFF
            | Ctrl.COUNT_INC_PC
            | Ctrl.COUNT_DEC_SP
        )
        uops[2] |= (
            Ctrl.ADDR_ASSERT_SP
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_LSB
            | Ctrl.XFER_ASSERT_PC
            | Ctrl.COUNT_DEC_SP
        )
        uops[3] |= (
            Ctrl.ADDR_ASSERT_SP
            | Ctrl.DBUS_LOAD_MEM
            | Ctrl.DBUS_ASSERT_MSB
            | Ctrl.XFER_ASSERT_PC
        )
        uops[4] |= (
            Ctrl.ADDR_ASSERT_PC
            | Ctrl.OFFSET_EN
            | Ctrl.XFER_ASSERT_ADDR
            | Ctrl.XFER_LOAD_PC
        )
    elif OP == Op.JSR_X:
        return jsr_ptr(GPP.X)
    elif OP == Op.JSR_Y:
        return jsr_ptr(GPP.Y)
    elif OP == Op.RTS:
        uops[2] |= (
            Ctrl.ADDR_ASSERT_SP
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_PCH
            | Ctrl.COUNT_INC_SP
        )
        uops[3] |= (
            Ctrl.ADDR_ASSERT_SP
            | Ctrl.DBUS_ASSERT_MEM
            | Ctrl.DBUS_LOAD_PCL
            | Ctrl.COUNT_INC_SP
            | Ctrl.CTRL_RST_USEQ
        )
    elif OP == Op.RTI:
        uops[1] |= Ctrl.CTRL_SET_UBR | Ctrl.ALU_SEI
        uops[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_PCH | Ctrl.COUNT_INC_SP
        uops[3] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_PCL | Ctrl.COUNT_INC_SP
        uops[4] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_SR | Ctrl.COUNT_INC_SP | Ctrl.CTRL_RST_USEQ

    elif OP == Op.JMP_ABS:
        return jmp_abs(flags.unconditional)
    elif OP == Op.JMP_REL:
        return jmp_rel(flags.unconditional)
    elif OP == Op.JMP_X:
        return jmp_ptr(flags.unconditional, GPP.X)
    elif OP == Op.JMP_Y:
        return jmp_ptr(flags.unconditional, GPP.Y)

    elif OP == Op.JO_ABS:
        return jmp_abs(flags.is_overflow)
    elif OP == Op.JO_REL:
        return jmp_rel(flags.is_overflow)
    elif OP == Op.JO_X:
        return jmp_ptr(flags.is_overflow, GPP.X)
    elif OP == Op.JO_Y:
        return jmp_ptr(flags.is_overflow, GPP.Y)

    elif OP == Op.JNO_ABS:
        return jmp_abs(flags.is_not_overflow)
    elif OP == Op.JNO_REL:
        return jmp_rel(flags.is_not_overflow)
    elif OP == Op.JNO_X:
        return jmp_ptr(flags.is_not_overflow, GPP.X)
    elif OP == Op.JNO_Y:
        return jmp_ptr(flags.is_not_overflow, GPP.Y)

    elif OP == Op.JS_ABS:
        return jmp_abs(flags.is_negative)
    elif OP == Op.JS_REL:
        return jmp_rel(flags.is_negative)
    elif OP == Op.JS_X:
        return jmp_ptr(flags.is_negative, GPP.X)
    elif OP == Op.JS_Y:
        return jmp_ptr(flags.is_negative, GPP.Y)

    elif OP == Op.JNS_ABS:
        return jmp_abs(flags.is_not_negative)
    elif OP == Op.JNS_REL:
        return jmp_rel(flags.is_not_negative)
    elif OP == Op.JNS_X:
        return jmp_ptr(flags.is_not_negative, GPP.X)
    elif OP == Op.JNS_Y:
        return jmp_ptr(flags.is_not_negative, GPP.Y)

    elif OP == Op.JE_ABS:
        return jmp_abs(flags.is_equal)
    elif OP == Op.JE_REL:
        return jmp_rel(flags.is_equal)
    elif OP == Op.JE_X:
        return jmp_ptr(flags.is_equal, GPP.X)
    elif OP == Op.JE_Y:
        return jmp_ptr(flags.is_equal, GPP.Y)

    elif OP == Op.JNE_ABS:
        return jmp_abs(flags.is_not_equal)
    elif OP == Op.JNE_REL:
        return jmp_rel(flags.is_not_equal)
    elif OP == Op.JNE_X:
        return jmp_ptr(flags.is_not_equal, GPP.X)
    elif OP == Op.JNE_Y:
        return jmp_ptr(flags.is_not_equal, GPP.Y)

    elif OP == Op.JC_ABS:
        return jmp_abs(flags.is_carry)
    elif OP == Op.JC_REL:
        return jmp_rel(flags.is_carry)
    elif OP == Op.JC_X:
        return jmp_ptr(flags.is_carry, GPP.X)
    elif OP == Op.JC_Y:
        return jmp_ptr(flags.is_carry, GPP.Y)

    elif OP == Op.JNC_ABS:
        return jmp_abs(flags.is_not_carry)
    elif OP == Op.JNC_REL:
        return jmp_rel(flags.is_not_carry)
    elif OP == Op.JNC_X:
        return jmp_ptr(flags.is_not_carry, GPP.X)
    elif OP == Op.JNC_Y:
        return jmp_ptr(flags.is_not_carry, GPP.Y)

    elif OP == Op.JBE_ABS:
        return jmp_abs(flags.is_below_or_equal)
    elif OP == Op.JBE_REL:
        return jmp_rel(flags.is_below_or_equal)
    elif OP == Op.JBE_X:
        return jmp_ptr(flags.is_below_or_equal, GPP.X)
    elif OP == Op.JBE_Y:
        return jmp_ptr(flags.is_below_or_equal, GPP.Y)

    elif OP == Op.JA_ABS:
        return jmp_abs(flags.is_above)
    elif OP == Op.JA_REL:
        return jmp_rel(flags.is_above)
    elif OP == Op.JA_X:
        return jmp_ptr(flags.is_above, GPP.X)
    elif OP == Op.JA_Y:
        return jmp_ptr(flags.is_above, GPP.Y)

    elif OP == Op.JL_ABS:
        return jmp_abs(flags.is_less)
    elif OP == Op.JL_REL:
        return jmp_rel(flags.is_less)
    elif OP == Op.JL_X:
        return jmp_ptr(flags.is_less, GPP.X)
    elif OP == Op.JL_Y:
        return jmp_ptr(flags.is_less, GPP.Y)

    elif OP == Op.JGE_ABS:
        return jmp_abs(flags.is_greater_or_equal)
    elif OP == Op.JGE_REL:
        return jmp_rel(flags.is_greater_or_equal)
    elif OP == Op.JGE_X:
        return jmp_ptr(flags.is_greater_or_equal, GPP.X)
    elif OP == Op.JGE_Y:
        return jmp_ptr(flags.is_greater_or_equal, GPP.Y)

    elif OP == Op.JLE_ABS:
        return jmp_abs(flags.is_less_or_equal)
    elif OP == Op.JLE_REL:
        return jmp_rel(flags.is_less_or_equal)
    elif OP == Op.JLE_X:
        return jmp_ptr(flags.is_less_or_equal, GPP.X)
    elif OP == Op.JLE_Y:
        return jmp_ptr(flags.is_less_or_equal, GPP.Y)

    elif OP == Op.JG_ABS:
        return jmp_abs(flags.is_greater)
    elif OP == Op.JG_REL:
        return jmp_rel(flags.is_greater)
    elif OP == Op.JG_X:
        return jmp_ptr(flags.is_greater, GPP.X)
    elif OP == Op.JG_Y:
        return jmp_ptr(flags.is_greater, GPP.Y)

    elif OP == Op.MUSTEQ_A_IMM:
        return musteq_imm(GPR.A)
    elif OP == Op.MUSTEQ_B_IMM:
        return musteq_imm(GPR.B)
    elif OP == Op.MUSTEQ_C_IMM:
        return musteq_imm(GPR.C)
    elif OP == Op.MUSTEQ_D_IMM:
        return musteq_imm(GPR.D)

    else:
        return [-1]

    return uops


def make_extended(uops: list[int], OP: int) -> list[int]:
    if not OP & 0b1_00000000:
        return uops

    corrected = BASE.copy()

    for i in range(2, 8):
        corrected[i] = uops[i - 1]

    return corrected


def get_cycles(uops: list[int]) -> int:
    if not any(uops):
        raise ValueError("All cycles are null")

    for i, word in enumerate(reversed(uops)):
        if word:
            break

    return 8 - i


def get_size(uops: list[int]) -> int:
    return sum(
        bool(word & Ctrl.ADDR_ASSERT_PC) and bool(word & Ctrl.DBUS_ASSERT_MEM)
        for word in uops
    )


def write_ucode(ucode: list[int], file_name_format: str) -> None:
    roms: list[list[int]] = [[], [], [], []]

    # Split the 32b words into 4x 8b words
    for addr, word in enumerate(ucode):
        for i in range(4):
            byte = (word & (255 << (8 * i))) >> (8 * i)
            roms[i].append(byte)

    names = (file_name_format.format(i) for i in range(4))

    # Write each ROM list to disk
    for rom, name in zip(roms, names):
        with open(OUTPUT_LOCATION / name, "wb") as f:
            for uop in rom:
                f.write(uop.to_bytes(1, "big"))


def main() -> None:
    ucode, lens, sizes = [], [], []
    for addr in range(2**15):
        state = State.from_packed(addr)
        uops = get_uops(state)

        if uops[0] == -1:
            mode, flags, nop = state.mode, state.flags, Op.NOP
            corrected = get_uops(State(state.mode, state.flags, Op.NOP))
            if corrected[0] == -1:
                raise RuntimeError(mode, flags, nop)
        else:
            corrected = make_extended(uops, state.opcode)
            if state.mode == Mode.FETCH and state.opcode != Op.EXT:
                lens.append(get_cycles(corrected))
                sizes.append(get_size(corrected))

        ucode.extend(corrected)

    print(f"Clocks per Instruction estimate: {sum(lens) / len(lens):.2f}")
    print(f"Bytes per Instruction estimate: {sum(sizes) / len(sizes):.2f}")

    write_ucode(ucode, "microcode{}.bin")
    print(Ctrl.decode(ucode[0b110000000000000000]))
    print()
    print(Ctrl.decode(ucode[0b110000000000000001]))
    print()
    print(Ctrl.decode(ucode[0b110000000000000010]))
    print()


if __name__ == "__main__":
    main()
