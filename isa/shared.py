from dataclasses import dataclass
from enum import Enum
from typing import Union


class Buses(Enum):
    DATA8 = "data"
    ADDR16 = "addr"
    LHS = "lhs"
    RHS = "rhs"
    DATA16 = "data16"


@dataclass
class Component:
    name: str
    width: int
    buses: tuple[Buses, ...]


class Units(Enum):
    IMM = "I"
    AREG = "A"
    BREG = "B"
    CREG = "C"
    ACC = "E"

    SP = "SP"
    IR = "IR"
    SR = "SR"

    TLREG = "TL"
    THREG = "TH"

    XREG = "X"
    XLREG = "XL"
    XHREG = "XH"

    YREG = "Y"
    YLREG = "YL"
    YHREG = "YH"

    PC = "PC"
    PCL = "PCL"
    PCH = "PCH"


class Flags(Enum):
    ZERO = "Z"
    CARRY = "C"
    NEGATIVE = "N"
    OVERFLOW = "V"
    LOGICAL_CARRY = "L"
    INTERRUPT_INHIBIT = "I"


@dataclass
class Opcode:
    name: str
    operands: int = 0
    desc: str = ""

    def __repr__(self) -> str:
        rstr = f"Opcode({self.name})"
        rstr += f", {self.operands}"

        if self.desc:
            rstr += f", {self.desc}"

        rstr += ")"
        return rstr
