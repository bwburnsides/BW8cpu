from dataclasses import dataclass
import functools as ft
import itertools as it
from typing import Iterable, Sequence
from shared import Opcode, Units


@dataclass
class ALUInstruction:
    name: str
    commutative: bool
    replacement: bool
    operands: int


BinInst = ft.partial(ALUInstruction, operands=2)
UnyInst = ft.partial(ALUInstruction, operands=1, commutative=False, replacement=False)

instructions = (
    BinInst("ADD", True, False),
    BinInst("ADC", True, True),
    BinInst("SUB", False, False),
    BinInst("SBC", False, True),
    BinInst("AND", True, False),
    BinInst("OR", True, False),
    BinInst("XOR", True, False),
    UnyInst("NOT"),
    UnyInst("LSL"),
    UnyInst("ROL"),
    UnyInst("LSR"),
    UnyInst("ASR"),
    UnyInst("ROR"),
    UnyInst("INC"),
    UnyInst("DEC"),
)


def combinatoric_factory(inst: ALUInstruction, bank: Iterable) -> Iterable:
    if inst.commutative:
        if inst.replacement:
            return it.combinations_with_replacement(bank, r=inst.operands)
        return it.combinations(bank, r=inst.operands)
    if inst.replacement:
        return it.product(bank, repeat=inst.operands)
    return it.permutations(bank, r=inst.operands)


def alu_opcodes(regs: Sequence[Units]) -> list[Opcode]:
    opcodes = []
    for inst in instructions:
        for operands in combinatoric_factory(inst, regs):
            operand_ct = 1 if Units.IMM in operands else 0
            name = " ".join(it.chain([inst.name], [op.name for op in operands]))
            opcodes.append(Opcode(name, operand_ct))

    modes = "DEC", "INC"
    for mode, reg in it.product(modes, [Units.XREG, Units.YREG]):
        opcodes.append(Opcode(mode))
    return opcodes
