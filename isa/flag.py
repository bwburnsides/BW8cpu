import itertools as it
from shared import Opcode, Flags

# Zero
# Carry
# Negative
# Overflow
# Logical Carry
# Interrupt Inhibit

modes = "SE", "CL"


def flag_opcodes() -> list[Opcode]:
    return [Opcode(f"{mode}{flag.value}") for mode, flag in it.product(modes, Flags)]
