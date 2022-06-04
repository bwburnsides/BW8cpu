from enum import IntEnum
from dataclasses import dataclass


class ShiftFunc(IntEnum):
    LHS = 0
    SRC = 1
    ASR = 2
    ZERO = 3
    DONT_CARE = 3


class LogicFunc(IntEnum):
    ZERO = 0b0000
    _255 = 0b1111
    A = LHS = 0b1010
    B = RHS = 0b1100
    notA = notLHS = 0b0101
    notB = notRHS = 0b0011
    OR = 0b1110
    AND = 0b1000
    XOR = 0b0110
    DONT_CARE = _255


class SumFunc(IntEnum):
    ZERO = 0b00
    Cf = 0b01
    ONE = 0b11
    DONT_CARE = ONE


class CfMode(IntEnum):
    SET = 0b000
    C_SHIFT = 0b001
    C_SUM = 0b010
    CLEAR = 0b011
    NO_CHANGE = 0b111


class ZVNfMode(IntEnum):
    SET = 0b00
    NEW = 0b01
    CLEAR = 0b10
    NO_CHANGE = 0b11


ZfMode = ZVNfMode
VfMode = ZVNfMode
NfMode = ZVNfMode


class IfMode(IntEnum):
    SET = 0b00
    CLEAR = 0b01
    NO_CHANGE = 0b11


@dataclass
class ALUOp:
    name: str
    value: int
    shift_func: ShiftFunc = ShiftFunc.DONT_CARE
    logic_func: LogicFunc = LogicFunc.DONT_CARE
    sum_func: SumFunc = SumFunc.DONT_CARE
    c_f: CfMode = CfMode.NO_CHANGE
    z_f: ZfMode = ZfMode.NO_CHANGE
    v_f: VfMode = VfMode.NO_CHANGE
    n_f: NfMode = NfMode.NO_CHANGE
    i_f: IfMode = IfMode.NO_CHANGE


alu_ops = (
    ALUOp(
        name="NOP",
        value=0,
        shift_func=ShiftFunc.ZERO,
        logic_func=LogicFunc.ZERO,
        sum_func=SumFunc.ZERO,
    ),
    ALUOp(
        name="ADC",
        value=1,
        shift_func=ShiftFunc.LHS,
        logic_func=LogicFunc.RHS,
        sum_func=SumFunc.Cf,
        c_f=CfMode.C_SUM,
        z_f=ZfMode.NEW,
        v_f=VfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="SBC",
        value=2,
        shift_func=ShiftFunc.LHS,
        logic_func=LogicFunc.notRHS,
        sum_func=SumFunc.Cf,
        c_f=CfMode.C_SUM,
        z_f=ZfMode.NEW,
        v_f=VfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="INC",
        value=3,
        shift_func=ShiftFunc.ZERO,
        logic_func=LogicFunc.RHS,
        sum_func=SumFunc.ONE,
        c_f=CfMode.C_SUM,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="DEC",
        value=4,
        shift_func=ShiftFunc.LHS,
        logic_func=LogicFunc._255,
        sum_func=SumFunc.ZERO,
        c_f=CfMode.C_SUM,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="AND",
        value=5,
        shift_func=ShiftFunc.ZERO,
        logic_func=LogicFunc.AND,
        sum_func=SumFunc.ZERO,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="OR",
        value=6,
        shift_func=ShiftFunc.ZERO,
        logic_func=LogicFunc.OR,
        sum_func=SumFunc.ZERO,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="XOR",
        value=7,
        shift_func=ShiftFunc.ZERO,
        logic_func=LogicFunc.XOR,
        sum_func=SumFunc.ZERO,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="NOT",
        value=8,
        shift_func=ShiftFunc.ZERO,
        logic_func=LogicFunc.notRHS,
        sum_func=SumFunc.ZERO,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="SRC",
        value=9,
        shift_func=ShiftFunc.SRC,
        logic_func=LogicFunc.ZERO,
        sum_func=SumFunc.ZERO,
        c_f=CfMode.C_SHIFT,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="ASR",
        value=10,
        shift_func=ShiftFunc.ASR,
        logic_func=LogicFunc.ZERO,
        sum_func=SumFunc.ZERO,
        c_f=CfMode.C_SHIFT,
        z_f=ZfMode.NEW,
        n_f=NfMode.NEW,
    ),
    ALUOp(
        name="SEI",
        value=11,
        i_f=IfMode.SET,
    ),
    ALUOp(
        name="CLI",
        value=12,
        i_f=IfMode.CLEAR,
    ),
    ALUOp(
        name="SEC",
        value=13,
        c_f=CfMode.SET,
    ),
    ALUOp(
        name="CLC",
        value=14,
        c_f=CfMode.CLEAR,
    ),
    ALUOp(
        name="CLV",
        value=15,
        v_f=VfMode.CLEAR,
    ),
)

header = [
    "ALU-OP",
    "Sel-Shift-1",
    "Sel-Shift-0",
    "Sel-Logic-3",
    "Sel-Logic-2",
    "Sel-Logic-1",
    "Sel-Logic-0",
    "Sel-Cin-1",
    "Sel-Cin-0",
    "Sel-Cf-2",
    "Sel-Cf-1",
    "Sel-Cf-0",
    "Sel-Zf-1",
    "Sel-Zf-0",
    "Sel-Vf-1",
    "Sel-Vf-0",
    "Sel-Nf-1",
    "Sel-Nf-0",
    "Sel-If-1",
    "Sel-If-0",
]


def spaces(iterable: str) -> str:
    return " ".join(iterable)


test_lines = []

for op in alu_ops:
    test_lines.append(f"# {op.name}")
    io = [
        f"{op.value}",
        spaces(f"{op.shift_func:02b}"),
        spaces(f"{op.logic_func:04b}"),
        spaces(f"{op.sum_func:02b}"),
        spaces(f"{op.c_f:03b}"),
        spaces(f"{op.z_f:02b}"),
        spaces(f"{op.v_f:02b}"),
        spaces(f"{op.n_f:02b}"),
        spaces(f"{op.i_f:02b}"),
    ]

    test_lines.append(spaces(io))

print(spaces(header))
print("\n".join(test_lines))
