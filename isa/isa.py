from enum import Enum
import itertools as it
from collections import namedtuple
from pprint import pprint
from alu import alu_opcodes
from mov import mov_opcodes
from flag import flag_opcodes
from shared import Units, Opcode, Flags


def jump_opcodes():
    modes = "C", "S"
    jumps = [
        Opcode(f"J{flag.value}{mode}")
        for flag, mode in it.product(Flags, modes)
        if flag != Flags.INTERRUPT_INHIBIT
    ]
    jumps.append(Opcode("JMP", 2))  # unconditional jump
    jumps.append(Opcode("JSR", 2))  # jump to subroutine
    jumps.append(Opcode("RTS"))  # return from subroutine
    jumps.append(Opcode("RTI"))  # return from interrupt service routine
    return jumps


def loadstore_opcodes():
    Mode = namedtuple("Mode", ["name", "operand_ct"])
    modes = {"LD": Mode("LD", 2), "ST": Mode("ST", 2), "LI": Mode("LI", 1)}
    codes = []
    for mode in modes.values():
        for reg in (Units.AREG, Units.BREG, Units.CREG):
            codes.append(Opcode(f"{mode.name}{reg.name[0]}", mode.operand_ct))

    k = "ST"
    codes.append(Opcode(f"{k}{Units.ACC.value}", modes[k].operand_ct))
    return codes


def stack_opcodes():
    modes = "PH", "PL"
    names = "A", "B", "C", "S", "P", "X", "Y"
    codes = [Opcode(f"{mode}{name}") for mode, name in it.product(modes, names)]
    codes.append(Opcode("PHI", 1))  # push immediate value to stack
    codes.append(Opcode("PHE"))  # Push accumulator to stack
    return codes


opcodes = [
    Opcode("HLT"),
    Opcode("NOP"),
    *alu_opcodes([Units.IMM, Units.AREG, Units.BREG, Units.CREG]),
    *flag_opcodes(),
    *jump_opcodes(),
    *loadstore_opcodes(),
    *stack_opcodes(),
    *mov_opcodes(),
]

print("Number of opcodes: ", len(opcodes))

counter = {}
for opcode in opcodes:
    ct = opcode.operands
    if ct not in counter:
        counter[ct] = 0
    counter[ct] += 1

for operands, amount in counter.items():
    print(f"{operands} Operands: {amount}")

with open("single_operand.txt", "w") as f:
    for opcode in opcodes:
        if opcode.operands == 1:
            print(opcode, file=f)

with open("double_operand.txt", "w") as f:
    for opcode in opcodes:
        if opcode.operands == 2:
            print(opcode, file=f)

with open("all_opcodes.txt", "w") as f:
    for opcode in opcodes:
        print(opcode, file=f)